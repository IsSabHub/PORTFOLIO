# Booking.com Hotel Scraper

This Python script scrapes hotel names from Booking.com search results and saves them to a CSV file.

## Features

* Scrapes hotel names from Booking.com search results.
* Saves the extracted data to a CSV file.
* Uses `requests` library to fetch the webpage.
* Uses `BeautifulSoup` library to parse the HTML content.
* Handles pagination to scrape multiple pages (currently not implemented, but can be added).

## Requirements

* Python 3.6 or higher
* `requests` library
* `beautifulsoup4` library

## Installation

1. Install the required libraries:

   ```bash
   pip install requests beautifulsoup4
Usage
Modify the url variable:

Replace the example URL with the Booking.com search results URL you want to scrape.
Run the script:

Bash
python booking_scraper.py

The script creates a directory named web_scraping_results (if it doesn't exist) and saves the extracted hotel names in a CSV file named hotels.csv within that directory.

Customization
Pagination:
To scrape multiple pages, you can modify the script to iterate through the pagination links on the Booking.com search results page.
Extract the URLs of the next pages and fetch them in a loop.
Data extraction:
You can modify the script to extract additional information like hotel prices, ratings, addresses, etc.
Inspect the HTML elements using your browser's developer tools to identify the relevant data.
Disclaimer
This script is for educational and research purposes only.
Use it responsibly and respect the Booking.com Terms of Service.
Web scraping may be against the terms of service of some websites. Use this script at your own risk.
The author is not responsible for any misuse of this script.