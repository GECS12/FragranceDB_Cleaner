import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def get_brand_urls():
    # Initialize the Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Open the webpage
    driver.get("https://mass-perfumarias.pt/perfumes.html")

    # Wait for the page to load completely
    time.sleep(1)

    # Find the "Marca" filter options title and click it
    marca_filter = driver.find_element(By.CSS_SELECTOR, 'div.filter-options-item.filter-options-item-brand_mass .filter-options-title')
    ActionChains(driver).move_to_element(marca_filter).click().perform()

    # Wait for the options to expand
    time.sleep(1)

    # Now, you can proceed to extract the brands
    brands = driver.find_elements(By.CSS_SELECTOR, 'div.filter-options-item.filter-options-item-brand_mass li.item')
    brand_urls= []
    for brand in brands:
        brand_name = brand.find_element(By.CSS_SELECTOR, 'span.swissup-option-label').text
        brand_url = brand.find_element(By.CSS_SELECTOR, 'a.swissup-aln-item').get_attribute('href')
        brand_urls.append((brand_name, brand_url))
        print(brand_name, brand_url)

    # Close the driver
    driver.quit()

    return brand_urls

