# -*- coding: utf-8 -*-
"""scraper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-2nPPnpDXAq0X61bN-Qj4xUmw4GNfBBT
"""

#Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

#Function to scrape a URL and extract table data
def scrape_table(url, year, session):
    try:
        #Use session with retry strategy
        response = session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', id='combine')  #Target Combine table

        if table is None:
            print(f"No Combine table found at {url}")
            return None, None

        #Extract headers from thead
        header_row = table.find('thead')
        if not header_row:
            print(f"No header row found for {year}")
            return None, None
        headers = [th.text.strip() for th in header_row.find_all('th')]

        #Extract rows from tbody
        body = table.find('tbody')
        if not body:
            print(f"No body found for {year}")
            return None, None
        rows = []
        for tr in body.find_all('tr'):
            #Get Player from <th>
            player_cell = tr.find('th')
            if not player_cell:
                continue  #Skip rows without a player
            player = player_cell.text.strip()

            #Get remaining columns from <td>
            cells = [td.text.strip() for td in tr.find_all('td')]
            if not cells:  #Skip if no data
                continue

            #Combine: Player + other columns + Year
            row = [player] + cells + [year]
            rows.append(row)

        print(f"Headers: {len(headers)}, Data columns: {len(rows[0]) if rows else 0}")
        return headers, rows

    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error for {year}: {e}")
        return None, None

#Set up a session with retry strategy
session = requests.Session()
retry_strategy = Retry(
    total=3,  #Retry up to 3 times
    status_forcelist=[429],  #Retry on 429 errors
    backoff_factor=2,  #Wait 2, 4, 8 seconds between retries
    raise_on_status=False  #Don't raise an exception if retries fail
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

#Scrape data
all_data = []
headers = None

for year in range(2000, 2026):
    url = f"https://www.pro-football-reference.com/draft/{year}-combine.htm"
    print(f"Scraping data for {year}...")
    year_headers, year_rows = scrape_table(url, year, session)

    if year_headers and year_rows:
        if headers is None:  #Set headers from first successful year
            headers = year_headers
            print(f"Initial headers set from {year}: {headers}")

        #Check column alignment
        expected_cols = len(headers) + 1  #+1 for Year
        for row in year_rows:
            if len(row) != expected_cols:
                print(f"Column mismatch for {year}: Expected {expected_cols}, Got {len(row)}, Row: {row}")
                #Pad or trim to match headers
                if len(row) < expected_cols:
                    row.extend([None] * (expected_cols - len(row)))
                elif len(row) > expected_cols:
                    row = row[:expected_cols]
            all_data.append(row)

        print(f"Successfully scraped {len(year_rows)} players for {year}")

    #Increased delay to avoid rate limiting
    sleep(5)  #Wait 5 seconds between requests

#Create DataFrame and save
if all_data:
    headers.append('Year')  #Add 'Year' to headers
    print(f"Final headers: {len(headers)}, Sample row columns: {len(all_data[0])}")
    df = pd.DataFrame(all_data, columns=headers)
else:
    print("No data collected. Check the website structure or connectivity.")