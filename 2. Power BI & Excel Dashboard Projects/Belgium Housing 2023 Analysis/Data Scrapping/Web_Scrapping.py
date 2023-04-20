import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

csv_file = open('immo_be.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Price', 'Location','Bedrooms', 'Bathrooms', 'Surface'])

for page_num in range(1, 50):
    url = f"www.websitetoscrape.com/yoursearch={page_num}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for article in soup.find_all('article', class_="li-PropertyCardV2List bg-white flex flex-row flex-wrap items-stretch rounded border border-grayeee cursor-pointer min-w-full md:min-h-32"):  
        title = article.find('h2', class_="mb-0 mr-auto text-sm text-gray777 uppercase")
        price = article.find('div', class_="price-component")
        location = article.find('h3', class_="text-black font-bold uppercase")
        ml1_elements = article.find_all('span', {'class': 'ml-1'})
        ml1_texts = [element.text for element in ml1_elements]

        # Extract the relevant information from ml1_texts
        bedrooms = ml1_texts[::3]
        bathrooms = ml1_texts[1::3]
        surface_area = ml1_texts[2::3]

         # Write the information to the CSV file
        for i in range(len(bedrooms)):
            if i < len(bathrooms) and i < len(surface_area):
        
                csv_writer.writerow([title, price, location, bedrooms[i], bathrooms[i], surface_area[i]])

csv_file.close()

df = pd.read_csv('immo_be.csv', encoding='ISO-8859-1')

df['Title'] = df['Title'].str.replace('<h2 class="mb-0 mr-auto text-sm text-gray777 uppercase">', '')
df['Title'] = df['Title'].str.replace('</h2>', '')
df['Title'] = df['Title'].str.replace(' à vendre', '')
df['Price'] = df['Price'].str.replace('<div class="price-component"><span>', '')
df['Price'] = df['Price'].str.replace('</span> <!-- --></div>', '')
df['Price'] = df['Price'].str.replace('<div class="price-component line-through text-input"><span>', '')
df['Location'] = df['Location'].str.replace('<h3 class="text-black font-bold uppercase">', '')
df['Location'] = df['Location'].str.replace('</h3>', '')

df.dropna(inplace=True)

df.to_csv('immo_be.csv', index=False)