# Base Scraper class
from BaseScraper.Base import BaseScraper

# to search for things using specific parameters
from selenium.webdriver.common.by import By

# wait for the page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime
from Logging.log import log_info

class Pidan(BaseScraper):
    def __init__(self, driver = None):
        url = [f'https://pidan.store/collections/all?page={i}' for i in range(1, 6)]
        super().__init__(url=url, driver=driver)
    
    def parse(self):
        self.data = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="CollectionProductGrid"]/ul//li'))
        )
    
    def clean_data(self):
        products = self.data
        self.data = {}
        for product in products:
            # skip the empty li tags
            if product.get_attribute('role') == 'presentation':
                continue

            # product url
            url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # image urls
            image_urls_raw = product.find_element(By.XPATH, "//*[@class='relative']//source").get_attribute('srcset').split(", ")
            image_urls = {}
            for image in image_urls_raw:
                image = image.split(" ")
                if ( image == [''] ):
                    continue
                image_urls[image[1] + " " +  image[2]] = image[0][2:]

            # product title
            title = product.find_element(By.CLASS_NAME, 'product-grid-title').text

            # price, regular_price, and onSale
            price_raw = product.find_element(By.XPATH, ".//div[@class='relative']/div[2]/div[2]").text
            onSale = "On Sale" in price_raw
            if not onSale:
                regular_price = price_raw
                price = price_raw
            else:
                price_raw = price_raw.split("\n")
                regular_price = price_raw[1]
                price = price_raw[-1].split(" ")[-1]
            
            self.data[title] = {
                "url": url,
                "image_urls": image_urls,
                "price_history": [
                    {
                        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "onSale": onSale,
                        "price": price,
                        "regular_price": regular_price,
                    }
                ],
            }
            


    def store(self):
        self.save_to_json("pidan.json")
        self.save_to_csv("pidan.csv")
        

