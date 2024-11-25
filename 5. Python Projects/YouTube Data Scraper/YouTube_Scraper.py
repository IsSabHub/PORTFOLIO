import os
import csv
import requests
import re
import json
from googleapiclient.discovery import build
import argparse
import time

# Liste de clés API
api_keys = ["YOUR API"]

current_key_index = 0
youtube = build("youtube", "v3", developerKey=api_keys[current_key_index])

state_file = "progress.json"

# Fonction pour basculer entre les clés API
def switch_api_key():
    global current_key_index, youtube
    current_key_index = (current_key_index + 1) % len(api_keys)
    youtube = build("youtube", "v3", developerKey=api_keys[current_key_index])
    print(f"Switched to API key: {api_keys[current_key_index]}")

# Fonction pour sauvegarder l'état
def save_state(region, keyword, page):
    state = {"region": region, "keyword": keyword, "page": page}
    with open(state_file, "w") as f:
        json.dump(state, f)
    print(f"Saved state: region={region}, keyword={keyword}, page={page}")

# Fonction pour charger l'état
def load_state():
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            return json.load(f)
    return {"region": None, "keyword": None, "page": 1}

# Fonction principale
def main(keywords, maxResults, maxPages, regions, minSubscribers):
    columns = [
        "channel_id", "channel_title", "subscriber_count", 
        "youtube_handle", "email", "discord", "twitter", "region", "keyword",
    ]
    if not os.path.exists("data.csv"):
        with open("data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)

    # Charger l'état de progression
    state = load_state()
    start_keyword = state["keyword"]
    start_region = state["region"]
    start_page = state["page"]

    for keyword in keywords:
        if start_keyword and keyword != start_keyword:
            continue  # Sauter les mots-clés déjà parcourus
        start_keyword = None  # Une fois que nous atteignons le bon mot-clé, continuer normalement

        for region in regions:
            if start_region and region != start_region:
                continue  # Sauter les régions déjà parcourues
            start_region = None  # Réinitialiser après avoir atteint la bonne région

            page = start_page
            start_page = 1  # Réinitialiser le compteur de pages pour les régions suivantes
            nextPageToken = None
            print(f"Fetching data for keyword: {keyword} in region: {region}")

            while page <= maxPages:
                try:
                    print(f"Fetching page {page} for keyword: {keyword} in region: {region}")
                    # Requête à l'API YouTube pour chercher des chaînes
                    request = youtube.search().list(
                        part="snippet",
                        maxResults=maxResults,
                        q=keyword,
                        type="channel",
                        regionCode=region,
                        pageToken=nextPageToken
                    )
                    response = request.execute()

                    for item in response["items"]:
                        channel_id = item["snippet"]["channelId"]
                        channel_title = item["snippet"]["title"]
                        youtube_handle = f"@{item['snippet'].get('customUrl', '')}"

                        # Récupérer les détails de la chaîne
                        channel_request = youtube.channels().list(
                            part="snippet,statistics",
                            id=channel_id
                        )
                        channel_response = channel_request.execute()

                        try:
                            stats = channel_response["items"][0]["statistics"]
                            subscriber_count = int(stats.get("subscriberCount", 0))
                        except (IndexError, KeyError, ValueError):
                            subscriber_count = 0

                        # Filtrer les chaînes avec un nombre d'abonnés insuffisant
                        if subscriber_count < minSubscribers:
                            print(f"Skipping channel {channel_title} ({channel_id}) with {subscriber_count} subscribers.")
                            continue

                        # Scraper les informations depuis la page "À propos"
                        about_url = f"https://www.youtube.com/channel/{channel_id}/about"
                        try:
                            page_content = requests.get(about_url).text
                        except Exception as e:
                            print(f"Failed to fetch About page for {channel_id}: {e}")
                            page_content = ""

                        email = ",".join(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", page_content)))
                        discord = ",".join(set(re.findall(r"discord(?:\.gg|app\.com)/[\w-]+", page_content)))
                        twitter = ",".join(set(re.findall(r"twitter\.com/[\w-]+", page_content)))

                        # Sauvegarder les données
                        with open("data.csv", "a", newline="", encoding="utf-8") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([
                                channel_id, channel_title, subscriber_count, 
                                youtube_handle, email, discord, twitter, region, keyword
                            ])

                    # Gestion de la pagination
                    nextPageToken = response.get("nextPageToken")
                    save_state(region, keyword, page)  # Sauvegarder l'état
                    if not nextPageToken:
                        break
                    page += 1

                except Exception as e:
                    if "quotaExceeded" in str(e):
                        print(f"Quota exceeded. Switching API key...")
                        switch_api_key()
                        time.sleep(60)
                        continue
                    else:
                        print(f"Error on page {page} for region {region}: {e}")
                        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", help="Comma-separated list of keywords to search for (e.g., gaming,streaming,vlog)", default="gaming")
    parser.add_argument("--maxresults", help="Max results per page (default: 50)", type=int, default=50)
    parser.add_argument("--maxpages", help="Max number of pages to fetch per region (default: 5)", type=int, default=20)
    parser.add_argument("--minsubscribers", help="Minimum number of subscribers to include (default: 100)", type=int, default=100)

    parser.add_argument(
        "--regions", 
        help="Comma-separated list of region codes (e.g., FR,GB,DE,CH,BE)", 
        default="FR"
    )
    args = parser.parse_args()

    keywords = args.keywords.split(",")
    maxResults = args.maxresults
    maxPages = args.maxpages
    regions = args.regions.split(",")
    minSubscribers = args.minsubscribers

    main(keywords, maxResults, maxPages, regions, minSubscribers)