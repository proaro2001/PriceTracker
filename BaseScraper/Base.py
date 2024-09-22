import os
import json
import csv
from abc import ABC, abstractmethod
from driver.driver import get_driver
from Logging.log import log_function_call, log_info

class BaseScraper(ABC):
    def __init__(self, url, headless = True):
        """
        Initialize the scraper with the target URL and an empty data list.
        
        Args:
            url (str): The URL of the website to scrape.
        """
        self.headless = headless
        self.url = url
        self.data = []  # Initialize an empty list to store scraped data
        self.driver = get_driver(url, headless=headless)

    @log_function_call
    def fetch(self):
        """
        Fetch the content from the specified URL.
        
        This method should handle sending HTTP requests to retrieve the web page.
        """
        self.driver.get(self.url)

    @abstractmethod
    @log_function_call
    def parse(self):
        """
        Parse the fetched content to locate and extract the desired information.
        
        This method should analyze the HTML or JSON content and identify the data elements.
        """
        pass

    @abstractmethod
    @log_function_call
    def clean_data(self):
        """
        Clean and process the extracted data.
        
        This method should handle tasks like removing unwanted characters, handling missing values,
        and transforming data into a usable format.
        """
        pass

    @abstractmethod
    @log_function_call
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
        self.fetch()
        self.parse()
        self.clean_data()
        self.store()
        # ask for user input to close the browser
        quit = input("Press 'q' to quit: ")
        while self.headless and quit != 'q':
            quit = input("Press 'q' to quit: ")

        self.driver.quit()

    @log_function_call
    def save_to_json(self, filename="data.json", append=True):
        """
        Save the scraped data to a JSON file.
        Create a new file if it does not exist.
        Append to the file if it already exists when append is true.
        
        Args:
            filename (str): The name of the file where data will be saved.
            append (bool): Whether to append to an existing file or create a new one.
        """
        # Check if the file exists and load its contents if append mode is on
        if append and os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    existing_data = json.load(file)  # Load existing data
                except json.JSONDecodeError:
                    existing_data = []  # If there's an error, start with an empty list
        else:
            existing_data = []

        # Merge the new data into the existing data list
        existing_data.extend(self.data)

        # Write the updated data back to the file
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)
            log_info(f"Data saved to {filename}")

    @log_function_call
    def save_to_csv(self, filename = "data.csv", append=True):
        """
        Save the scraped data to a CSV file.
        Create a new file if it does not exist.
        Append to the file if it already exists when append is true.
        
        Args:
            filename (str): The name of the file where data will be saved.
            append (bool): Whether to append to an existing file or create a new one.
        
        """

        with open(filename, "a" if append else "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
            if not append or file.tell() == 0:
                writer.writeheader()
            writer.writerows(self.data)
            log_info(f"Data saved to {filename}")
