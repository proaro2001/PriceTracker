# import the keys module
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# to use the enter key like Enter, ESC, etc.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# helps to avoid adding to PATH
from webdriver_manager.chrome import ChromeDriverManager

import undetected_chromedriver as uc


def get_driver( headless=True):
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    if headless:
        options.add_argument("--headless")  # Run Chrome in headless mode

    # Essential arguments for environments like Docker
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument(f"user-agent={userAgent}")

    # Optional: Set a standard window size
    options.add_argument("window-size=1920,1080")

    # Set up Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def get_undetected_chromdriver (headless=True):
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    if headless:
        # options.add_argument("--headless=new")  # Run Chrome in headless mode
        options.add_argument("--headless")  # Run Chrome in headless mode

    # # Essential arguments for environments like Docker
    # options.add_argument("--no-sandbox")  
    # options.add_argument("--disable-dev-shm-usage")

    # Optional: Set a standard window size
    # options.add_argument("window-size=1920,1080")

    # Set up Chrome driver
    driver = uc.Chrome(options=options)
    return driver