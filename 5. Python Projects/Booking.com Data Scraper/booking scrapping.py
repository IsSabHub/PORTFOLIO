from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest
import os

# Define lists to store data
hotel_name = []

# Define URL and headers
url = "https://www.booking.com/searchresults.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaBWIAQGYAQ24ARfIAQzYAQHoAQGIAgGoAgO4AonNkboGwAIB0gIkZWJkNWY2NDItMmIzZi00MTdjLWIyNWQtMjM3MGQwNGJhYmZj2AIF4AIB&sid=613dae5b2e9bb1f26ee25027b91d5298&aid=304142&ss=Autriche&ssne=Autriche&ssne_untouched=Autriche&efdco=1&lang=fr&src=searchresults&dest_id=14&dest_type=country&group_adults=1&no_rooms=1&group_children=0&nflt=class%3D5%3Bht_id%3D206%3Bclass%3D4%3Bht_id%3D204"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

# Fetch the URL
result = requests.get(url, headers=headers)
if result.status_code == 200:
    print("Successfully fetched the webpage.")
else:
    print(f"Failed to fetch webpage. Status code: {result.status_code}")

# Parse the page content using html.parser
src = result.content
soup = BeautifulSoup(src, "html.parser")

# Find elements containing the needed info
hotel_names = soup.find_all("div", {"data-testid": "title"})

for name in hotel_names:
    hotel_name.append(name.text.strip())

# Create CSV file
output_dir = "web_scraping_results"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, "hotels.csv")

file_list = [hotel_name]
exported = zip_longest(*file_list)

with open(file_path, "w", newline='', encoding='utf-8') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['Hotel Name'])
    wr.writerows(exported)

print(f"Data exported to {file_path}")