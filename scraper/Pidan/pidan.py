# Base Scraper class
from BaseScraper.Base import BaseScraper

# to search for things using specific parameters
from selenium.webdriver.common.by import By

# wait for the page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime

class Pidan(BaseScraper):
    def __init__(self, headless = True):
        super().__init__("https://teddybob.ca/collections/pidan-cat-litter", headless=headless)
    
    def parse(self):
        self.data = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="shopify-section-collection-template"]/div/div[2]/div'))
        )
    
    def clean_data(self):
        products = self.data.find_elements(By.XPATH, '//*[@id="shopify-section-collection-template"]/div/div[2]/div/div')
        self.data = [] # clear the data

        for product in products:
            # print(product.text)
            # print("")
            reviews_count = product.find_element(By.XPATH, './/div[5]')
            # rating = len(product.find_elements(By.CLASS_NAME, 'star-container yotpo-sr-star-full'))
            # print(rating)
            star_rating_elements = len(product.find_elements(By.CLASS_NAME, 'yotpo-sr-star-full'))
            title = product.find_element(By.CLASS_NAME, 'product-block__title')
            price = product.find_element(By.CLASS_NAME, 'product-price')
            onSale = "On Sale" in product.text
            price = price.text.split("\n")
            regular_price = price[2] if len(price) > 1 else price[0]
            price = price[0][6:] if len(price) > 1 else price[0]
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # put product data into self.data 
            self.data.append({
                "title": title.text,
                "price": price,
                "regular_price": regular_price,
                "onSale": onSale,
                "date": date,
                "reviews_count": reviews_count.text,
                "star_rating": star_rating_elements
            })

    def store(self):
        # store the data in a json file 
        self.save_to_json("pidan.json")
        self.save_to_csv("pidan.csv")

