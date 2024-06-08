import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import nest_asyncio
from datetime import datetime

nest_asyncio.apply()


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()


def normalize_text(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return ascii_text


def construct_brand_url(brand_name):
    # Normalize the brand name to remove accents
    brand_name = normalize_text(brand_name)
    # Replace '&' with '-' and remove special characters
    brand_slug = re.sub(r'[^a-z0-9]+', '-', brand_name.lower().replace('&', '-')).strip('-')
    return f"https://perfumes24h.com/perfumes/{brand_slug}/"


def scrape_fragrances(soup, base_url, brand):
    fragrances = []
    print("Started scraping brand: " + brand)
    try:
        products = soup.find_all('div', class_='item_producto')
        #print(products)
        for product in products:
            fragrance_name = ""
            price = 0.0
            quantity = 0.0
            link = ""

            # Brand
            brand_name = brand
            print("Brand Name found: " + brand_name)

            # Fragrance Name
            fragrance_name = product.find('div', class_='nombre_grupo').text.strip()
            print("Fragrance Name found: " + fragrance_name)

            # Link
            link_tags = product.find_all('a', href=True)
            if len(link_tags) > 1:
                link = link_tags[1]['href']
                print("Link found: " + link)
            if not link.startswith('http'):
                link = base_url + link
                print("Link found: " + link)

            # Quantity and Price
            variants = product.find('div', class_='contenedor_variantes').find_all('div', class_='item_tamanyo')
            for variant in variants:
                quantity_text = variant.text.strip()
                #print("Quantity text found " + quantity_text)
                if quantity_text = "set":

                quantity_match = re.search(r'(\d+)\s*ml', quantity_text, re.IGNORECASE)
                if quantity_match:
                    quantity = float(quantity_match.group(1))
                    print("Quantity post research found: " + str(quantity))

                price_text = variant['data-pp'].replace(',', '.')
                price = float(price_text)
                print(price)

                if fragrance_name and quantity and price and link:
                    fragrances.append({
                        'Brand': brand_name,
                        'Fragrance Name': fragrance_name,
                        'Quantity (ml)': quantity,
                        'Price (€)': price,
                        'Link': link,
                        'Website': "Perfumes24h"
                    })

    except Exception as e:
        print(f"Error while scraping brand {brand}: {e}")

    df = pd.DataFrame(fragrances)
    return df


async def get_all_brands(url):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url)
        soup = BeautifulSoup(response, 'html.parser')
        brands = []
        brand_divs = soup.find_all('div', id=re.compile('^letra_'))
        for brand_div in brand_divs:
            brand_name = brand_div['data-nombre_marca']
            brands.append(brand_name)
    return brands

def scraped_to_excel(fragrances):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'fragrances_PT_{timestamp}.xlsx'
    fragrances.to_excel(filename, index=False)
    path = r"D:\Drive Folder\FragrancesV2\fragrancePT_Cleaner\fragranceDB\scrapers\Perfumes24h"
    print(filename + " has been saved in " + path)

async def main():
    base_url = "https://perfumes24h.com/"
    brands_url = "https://perfumes24h.com/perfumes/"

    # Get all brands
    brands = ['Alejandro Sanz']
    #brands = await get_all_brands(brands_url)
    #brands = ['Alejandro sanz'', 'Laroche', 'Lauder', 'Lauren', 'Lempicka', 'Liu·jo', 'Lorenay', 'Mancera paris', 'Mickey mouse', 'Minnie mouse', 'Miyake', 'Mugler', 'Pertegaz', 'Pocoyo', 'Quorum', 'Rabanne', 'Real madrid c.f.', 'Reebok', 'Ricci', 'Rodríguez', 'Schlesser', 'Spiderman', 'Taylor', 'Teaology', 'Ted lapidus', 'Thierry mugler', 'Titto bluni', 'Tiziana terenzi', 'Tom ford', 'Tommy hilfiger', 'Tous', 'Trussardi', 'United colors of benetton', 'Valentino', 'Van cleef & arpels', 'Vanderbilt', 'Varon dandy', 'Vera wang', 'Versace', 'Vicky martín berrocal', 'Victor', "Victoria's secret", 'Victorinox', 'Victorio & lucchino', 'Viktor & rolf', 'Vince camuto', "Women'secret", 'Xerjoff', 'Yacht man', 'Yves saint laurent', 'Zadig & voltaire', 'Zaitsev', '4711']
    print(f"Total number of brands: {len(brands)}")
    scraped_brands = 0
    scraped_brands_list = []
    missed_brands_list = []
    missed_url_list = []
    all_data = []

    async with aiohttp.ClientSession() as session:
        for brand in brands:
            url = construct_brand_url(brand)
            print(url)
            try:
                response = await fetch(session, url)
                soup = BeautifulSoup(response, 'html.parser')

                fragrance_data = scrape_fragrances(soup, base_url, brand)
                print(fragrance_data)
                if not fragrance_data.empty:
                    print(f"Scraped data for {brand}:")
                    all_data.append(fragrance_data)
                    scraped_brands += 1
                    scraped_brands_list.append(brand)
                else:
                    missed_brands_list.append(brand)
                    missed_url_list.append(url)
                    print(f"No url found for {brand}")
            except Exception as e:
                print(f"Failed to scrape brand {brand}: {e}")

    if all_data:
        full_df = pd.concat(all_data, ignore_index=True)
        #scraped_to_excel(full_df)
        print(missed_brands_list)
        print(missed_url_list)
        #full_df.to_csv("scraped_fragrances.csv", index=False)
        #print("All data scraped and saved to scraped_fragrances.csv")





if __name__ == '__main__':
    asyncio.run(main())
