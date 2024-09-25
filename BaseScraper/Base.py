import time
import random
import os
import json
import csv
from abc import ABC, abstractmethod
from Logging.log import log_function_call, log_info

class BaseScraper(ABC):
    def __init__(self, url, driver=None):
        """
        Initialize the scraper with the target URL and an empty data list.
        
        Args:
            url (str): The URL of the website to scrape.
        """
        if driver is None:
            raise Exception("Driver is not provided")
        self.url = url
        self.data = {}  # Initialize an empty list to store scraped data
        self.driver = driver

    def fetch(self, url):
        """
        Fetch the content from the specified URL.
        
        This method should handle sending HTTP requests to retrieve the web page.
        """
        self.driver.get(url)

    @abstractmethod
    def parse(self):
        """
        Parse the fetched content to locate and extract the desired information.
        
        This method should analyze the HTML or JSON content and identify the data elements.
        """
        pass

    @abstractmethod
    def clean_data(self):
        """
        Clean and process the extracted data.
        
        This method should handle tasks like removing unwanted characters, handling missing values,
        and transforming data into a usable format.
        """
        pass

    @abstractmethod
    def store(self):
        """
        Store the cleaned data in a structured format.
        
        This method should save the data to a file (e.g., JSON, CSV) or a database.
        """
        pass

    def run(self):
        """
        Execute the scraping process by running all the steps in sequence.
        
        This method orchestrates the entire scraping workflow: fetching, parsing,
        cleaning, and storing the data.
        """
        for url in self.url:
            log_info(f"Fetching data from {url}")
            self.fetch(url)
            log_info(f"Parsing data")
            self.parse()
            log_info(f"Cleaning data")
            self.clean_data()
            log_info(f"Storing data")
            self.store()
            log_info(f"Data scraped successfully\n")
            # random sleep to avoid getting blocked
            time.sleep(random.randint(1, 5))
        # ask for user input to close the browser
        # quit = input("Press 'q' to quit: ")
        # while quit != 'q':
        #     quit = input("Press 'q' to quit: ")

        self.driver.quit()

    def save_to_json(self, filename="data.json", append=True):
        """
        Save the current data to a JSON file.
        Parameters:
        filename (str): The name of the file to save the data to. Defaults to "data.json".
        append (bool): If True, append to the existing file content. If False, overwrite the file. Defaults to True.
        The method checks if the file exists and loads its contents if append mode is enabled. It then updates the 
        existing data with the current data, either by appending to the price history of existing entries or adding 
        new entries. Finally, it writes the updated data back to the file.
        """
        # Check if the file exists and load its contents if append mode is on
        if append and os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    existing_data = json.load(file)  # Load existing data
                except json.JSONDecodeError:
                    existing_data = {}  # If there's an error, start with an empty list
        else:
            existing_data = {}

        for title, details in self.data.items():
            if title in existing_data.keys():
                # append the details.price_history to the existing data
                existing_data[title]["price_history"].extend(details["price_history"])
            else:
                existing_data[title] = details
        
        # Write the updated data back to the file
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)
            log_info(f"Data saved to {filename}")
        
    def save_to_csv(self, filename = "data.csv", append=True):
        """
        Save the scraped data to a CSV file.
        Create a new file if it does not exist.
        Append to the file if it already exists when append is true.
        
        Args:
            filename (str): The name of the file where data will be saved.
            append (bool): Whether to append to an existing file or create a new one.
        
        """

        # with open(filename, "a" if append else "w", newline='') as file:
        #     writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
        #     if not append or file.tell() == 0:
        #         writer.writeheader()
        #     writer.writerows(self.data)
        #     log_info(f"Data saved to {filename}")
        print("Saving to CSV is not implemented yet")
