# Base Scraper class
from BaseScraper.Base import BaseScraper

# to search for things using specific parameters
from selenium.webdriver.common.by import By

# wait for the page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime

class Teddybob(BaseScraper):
    def __init__(self, driver = None):
        super().__init__(url=["https://teddybob.ca/collections/pidan-cat-litter"], driver=driver)
    
    def parse(self):
        self.data = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="shopify-section-collection-template"]/div/div[2]/div'))
        )
    
    def clean_data(self):
        products = self.data.find_elements(By.XPATH, '//*[@id="shopify-section-collection-template"]/div/div[2]/div/div')
        self.data = {} # clear the data

        for product in products:
            url = product.find_element(By.CLASS_NAME, 'product-block__image')
            image_urls_raw = url.find_element(By.TAG_NAME, 'img').get_attribute('srcset').split(", ")
            # print(image_urls_raw)
            image_urls = {}
            for image in image_urls_raw:
                image = image.split(" ")
                if ( image == [''] ):
                    continue
                image_urls[image[1]] = image[0][2:]
                

            url = url.get_attribute('href')
            reviews_count = product.find_element(By.XPATH, './/div[5]')
            star_rating_elements = len(product.find_elements(By.CLASS_NAME, 'yotpo-sr-star-full'))
            title = product.find_element(By.CLASS_NAME, 'product-block__title').text
            price = product.find_element(By.CLASS_NAME, 'product-price')
            onSale = "On Sale" in product.text
            price = price.text.split("\n")
            regular_price = price[2] if len(price) > 1 else price[0]
            price = price[0][6:] if len(price) > 1 else price[0]
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.data[title] = {
                "url": url,
                "image_urls": image_urls,
                "price_history": [
                    {
                        "date": date,
                        "onSale": onSale,
                        "price": price,
                        "regular_price": regular_price,
                        "reviews_count": reviews_count.text,
                        "star_rating": star_rating_elements
                    }
                ],
            }
