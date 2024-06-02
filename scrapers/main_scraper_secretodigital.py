from typing import List, Any
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import nest_asyncio
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import openpyxl

nest_asyncio.apply()

# Function to create a session with retry logic
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Function to correct encoding issues
def fix_encoding(brand):
    return brand.replace('Ã', 'Ç')

def get_all_brands(url):
    response = requests_retry_session().get(url)
    web_content = response.content
    soup = BeautifulSoup(web_content, 'html.parser')
    select_element = soup.find('select', {'name': 'marca'})
    all_brands = [fix_encoding(option.get('value')) for option in select_element.find_all('option') if option.get('value')]
    return all_brands

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()

async def fetch_post(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.read()

async def get_soups(url, brand, total_pages, base_url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, total_pages + 1):
            if page == 1:
                response = await fetch_post(session, url, {'marca': brand})
                post_soup = BeautifulSoup(response.decode('latin1'), 'html.parser')
                soups = [post_soup]
                tasks.append(fetch_post(session, url, {'marca': brand}))
            else:
                next_page_url = f"{base_url}/index.php?PASE={15 * (page - 1)}&marca={brand}&buscado=&ID_CATEGORIA=&ORDEN=&precio1=&precio2=#PRODUCTOS"
                tasks.append(fetch(session, next_page_url))
        pages = await asyncio.gather(*tasks)
        for page in pages[1:]:
            page_soup = BeautifulSoup(page.decode('latin1'), 'html.parser')
            soups.append(page_soup)
    return soups

def get_total_pages(soup):
    page_info = soup.find('font', {'face': 'arial', 'size': '1'})
    total_pages = 1
    if page_info:
        text = page_info.get_text()
        if "de" in text:
            try:
                total_pages = int(text.split("de")[-1].strip())
            except ValueError:
                pass
    return total_pages

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def scrape_fragrances(soups, base_url, brand):
    fragrances = []
    price_list = []

    for soup in soups:
        for td in soup.find_all('td', class_='padd_33'):
            a_tags = td.find_all('a', href=True)
            if a_tags:
                for a_tag in a_tags:
                    if a_tag.text.strip():
                        full_text = a_tag.text.strip()
                        link = base_url + a_tag['href'].replace('&amp;', '&')
                        quantity_match = re.search(r'(\d+)\s*ML', full_text, re.IGNORECASE)
                        if quantity_match:
                            quantity = quantity_match.group(1) + ' ML'
                            name = full_text.replace(quantity_match.group(0), '').strip().rstrip('@')
                            if '@' in full_text:
                                name += "- Tester"
                        else:
                            continue
                        fragrances.append({
                            'Brand': brand,
                            'Fragrance Name': name,
                            'Quantity (ml)': quantity,
                            'Price (€)': 0.0,
                            'Link': link
                        })
        for price_elem in soup.find_all('span', class_='productSpecialPrice'):
            text = price_elem.get_text()
            parts = text.split()
            if len(parts) > 1:
                price = float(parts[-2].replace('€', ''))
                price_list.append(price)

    df = pd.DataFrame(fragrances)
    for i, price in enumerate(price_list):
        if i < len(df):
            df.at[i, 'Price (€)'] = price

    print(f"{brand} has {len(df)} fragrances")
    return df

async def main():
    url = "https://perfumedigital.es/"
    base_url = "https://perfumedigital.es/"
    brands = get_all_brands(url)
    all_fragrances = pd.DataFrame(columns=['Brand', 'Fragrance Name', 'Quantity (ml)', 'Price (€)', 'Link'])

    for brand in brands:
        try:
            response = requests_retry_session().post(f"{url}/index.php", data={'marca': brand})
            initial_soup = BeautifulSoup(response.content.decode('latin1'), 'html.parser')
            total_pages = get_total_pages(initial_soup)
            soups = await get_soups(url, brand, total_pages, base_url)
            fragrance_data = scrape_fragrances(soups, base_url, brand)
            if not fragrance_data.empty:
                all_fragrances = pd.concat([all_fragrances, fragrance_data], ignore_index=True)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching brand {brand}: {e}")

    all_fragrances.to_excel('fragrances.xlsx', index=False)
    print("Data exported to fragrances.xlsx")

if __name__ == '__main__':
    asyncio.run(main())
