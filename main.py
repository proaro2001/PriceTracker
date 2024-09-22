import schedule
import time
from scraper.Pidan.pidan import Pidan
from Logging.log import log_info

# Function to run the scraping task
def run_script():
    pidan = Pidan(headless=True)
    pidan.run()
    log_info("Scraping complete\n")

# Schedule the script to run every day at 00:00
schedule.every().day.at("00:00").do(run_script)

# Keep the script running to execute the scheduled task
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute if it's time to run the task