# YouTube Channel Data Extractor

This Python script extracts data from YouTube channels based on specified keywords and regions. It uses the YouTube Data API v3 to search for channels and scrape additional information from their "About" page.

## Features

* Keyword-based search:  Find channels related to specific keywords (e.g., gaming, music, education).
* Region filtering:  Filter channels by region (e.g., US, UK, FR).
* Data extraction:  Extracts the following information:
    * Channel ID
    * Channel title
    * Subscriber count
    * YouTube handle (custom URL)
    * Email address (if available)
    * Discord link (if available)
    * Twitter handle (if available)
* Pagination:  Fetches multiple pages of results.
* API key management:  Uses a list of API keys to handle quota limits.
* Progress saving:  Saves the current progress to resume the extraction later.

## Requirements

* Python 3.6 or higher
* `google-api-python-client` library
* `requests` library

## Installation

1. Install the required libraries:

   ```bash
   pip install google-api-python-client requests
Obtain a YouTube Data API v3 key:

Go to the Google Cloud Console (https://console.cloud.google.com/).
Enable the YouTube Data API v3.
Create an API key.
Replace "YOUR API" in the script with your actual API key.

Usage
Bash
python youtube_channel_extractor.py --keywords "gaming,music" --regions "US,UK" --maxresults 50 --maxpages 10 --minsubscribers 1000
Utilisez ce code avec précaution.

Arguments:

--keywords: Comma-separated list of keywords to search for.
--regions: Comma-separated list of region codes (e.g., US, UK, FR).
--maxresults: Maximum number of results per page (default: 50).
--maxpages: Maximum number of pages to fetch per region (default: 20).
--minsubscribers: Minimum number of subscribers to include (default: 100).

The script saves the extracted data in a CSV file named data.csv.

Disclaimer
This script is for educational and research purposes only.
Use it responsibly and respect the YouTube Terms of Service.
The script scrapes data from the "About" page, which may not always be accurate or up-to-date.
The author is not responsible for any misuse of this script.