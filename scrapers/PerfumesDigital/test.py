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
from datetime import datetime
import db_utils
import aux_functions
import os


nest_asyncio.apply()

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
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

def fix_encoding(brand):
    replacements = {
        'Ã': 'Ç', 'Ã': 'Ö', 'Ã¤': 'ä', 'Ã«': 'ë', 'Ã¼': 'ü', 'Ã¶': 'ö', 'Ã': 'ß', 'Ã': 'É', 'Ã©': 'é',
        'Ã ': 'à', 'Ã¡': 'á', 'Ã¢': 'â', 'Ã£': 'ã', 'Ã¨': 'è', 'Ãª': 'ê', 'Ã¹': 'ù', 'Ãº': 'ú', 'Ã®': 'î',
        'Ã¯': 'ï', 'Ã´': 'ô', 'Ã§': 'ç', 'Ã±': 'ñ', 'Âº': 'º'
    }
    for key, value in replacements.items():
        brand = brand.replace(key, value)
    return brand

def get_all_brands(url):
    response = requests_retry_session().get(url)
    web_content = response.content
    soup = BeautifulSoup(web_content, 'html.parser')
    select_element = soup.find('select', {'name': 'marca'})
    all_brands = [normalize_text(fix_encoding(option.get('value'))) for option in select_element.find_all('option') if option.get('value')]
    return all_brands

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
                tasks.append(aux_functions.fetch(session, next_page_url))  # Use fetch from aux_functions
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
    normalized_text = unicodedata.normalize('NFKD', text)
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return ascii_text

def scrape_fragrances(soups, base_url, brand):
    fragrances = []
    print("Started scraping brand: " + brand)
    try:
        for soup in soups:
            product_tables = soup.find_all('table', class_='tableBox_output')
            for table in product_tables:
                rows = table.find_all('td', align='center')
                for row in rows:
                    fragrance_name = ""
                    price = 0.0
                    quantity = 0.0
                    link = ""

                    pic_td = row.find('td', class_='pic')
                    if pic_td:
                        a_tag = pic_td.find('a', href=True)
                        if a_tag:
                            link = base_url + a_tag['href'].replace('&amp;', '&')

                    desc_td = row.find('td', class_='vam')
                    if desc_td:
                        a_tag = desc_td.find('a', href=True)
                        if a_tag:
                            full_text = a_tag.text.strip()
                            full_text = full_text.encode('latin1').decode('utf-8')
                            full_text = normalize_text(full_text)
                            quantity_match = re.search(r'(\d+(\.\d+)?)\s*ML', full_text, re.IGNORECASE)
                            if quantity_match:
                                quantity = float(quantity_match.group(1))
                                if quantity.is_integer():
                                    quantity = int(quantity)
                                fragrance_name = full_text.replace(quantity_match.group(0), '').strip().rstrip('@')
                                if '@' in full_text:
                                    fragrance_name += "- Tester"
                            else:
                                continue

                    price_td = row.find('span', class_='productSpecialPrice')
                    if price_td:
                        price_text = price_td.get_text().split()
                        if len(price_text) > 1:
                            price = float(price_text[-2].replace('€', ''))

                    if fragrance_name and quantity and price and link:
                        fragrances.append({
                            'Brand': aux_functions.standardize_names(brand),
                            'Fragrance Name': aux_functions.standardize_names(fragrance_name),
                            'Quantity (ml)': quantity,
                            'Price (€)': price,
                            'Link': link,
                            'Website': "PerfumesDigital"
                        })
                        #print(fragrance_name + " " + str(price))

    except Exception as e:
        print(f"Error while scraping brand {brand}: {e}")

    df = pd.DataFrame(fragrances)
    return df

async def main():
    url = "https://perfumedigital.es/"
    base_url = "https://perfumedigital.es/"
    brands = get_all_brands(url)
    print(f"Total number of brands: {len(brands)}")
    all_fragrances = pd.DataFrame(columns=['Brand', 'Fragrance Name', 'Quantity (ml)', 'Price (€)', 'Link', 'Website'])
    scraped_brands = 0
    scraped_brands_list = []
    missed_brands_list = []
    for brand in brands[0:7]:  # You can limit the range for testing
        try:
            response = requests_retry_session().post(f"{url}/index.php", data={'marca': brand})
            initial_soup = BeautifulSoup(response.content.decode('latin1'), 'html.parser')
            total_pages = get_total_pages(initial_soup)
            soups = await get_soups(url, brand, total_pages, base_url)
            fragrance_data = scrape_fragrances(soups, base_url, brand)
            if not fragrance_data.empty:
                all_fragrances = pd.concat([all_fragrances, fragrance_data], ignore_index=True)
                scraped_brands += 1
                scraped_brands_list.append(brand)
            else:
                missed_brands_list.append(brand)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching brand {brand}: {e}")
            missed_brands_list.append(brand)
    print(f"Total number of brands scraped: {scraped_brands}")
    print(f"Total number of fragrances scraped: {len(all_fragrances)}")
    print(f"Total number of brands missed: {len(missed_brands_list)}")
    print(f"Missed brands: {missed_brands_list}")

    # Verify and correct the schema if needed
    #db_utils.verify_and_correct_schema('PT_fragrances', 'PerfumesDigital')

    # Save scraping to Excel
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    aux_functions.scrape_to_excel(all_fragrances, data_dir, 'PerfumesDigital')

    # Insert scraped data into the database
    aux_functions.scrape_to_db(all_fragrances, 'test_PT_fragrances', 'PerfumesDigital')


if __name__ == '__main__':
    asyncio.run(main())
