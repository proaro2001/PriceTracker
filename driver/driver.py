# import the keys module
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# to use the enter key like Enter, ESC, etc.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# helps to avoid adding to PATH
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(LINK, headless=True):
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    if headless:
        options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={userAgent}")

    # Set up Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(LINK)
    return driver
