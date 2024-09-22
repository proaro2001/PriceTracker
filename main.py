from scraper.Pidan.pidan import Pidan
from Logging.log import log_info

# Function to run the scraping task
def run_script():
    pidan = Pidan(headless=True)
    pidan.run()
    log_info("Scraping complete\n")


# Keep the script running to execute the scheduled task
if __name__ == "__main__":
    run_script()