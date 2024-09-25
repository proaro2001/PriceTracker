from scraper.Teddybob.teddybob import Teddybob
from Logging.log import log_info
from driver.driver import get_driver, get_undetected_chromdriver
from scraper.Pidan.pidan import Pidan

# Function to run the scraping task
def run_script():
    headless = True
    log_info("Starting the scraping process on Teddybob")
    teddybob = Teddybob( driver=get_driver(headless=headless))
    teddybob.run()

    log_info("Starting the scraping process on Pidan")
    pidan = Pidan( driver=get_undetected_chromdriver(headless=headless) )
    pidan.run()
    log_info("Scraping complete\n")


# Keep the script running to execute the scheduled task
if __name__ == "__main__":
    run_script()