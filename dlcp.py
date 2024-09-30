import requests
import bs4
from datetime import datetime
import pytz  # Timezone conversions
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PROG_NAME = sys.argv[0]

def get_daily_challenge():
    BASE_URL = 'https://leetcode.com'
    SCRAPE_URL = BASE_URL + '/problemset/'
    DAILY_Q_QUERY = 'envType=daily-question&envId=' + datetime.now(pytz.utc).strftime('%Y-%m-%d')
    logger = open('logs/dlcp.log', 'a')  # Use 'a' to append logs

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, timeout=60, poll_frequency=.2)

    try:
        driver.get(SCRAPE_URL)
        content = driver.page_source
        soup = bs4.BeautifulSoup(content, features="html.parser")

        # Search for the daily question URL
        for a in soup.body.find_all('a', href=True):
            if DAILY_Q_QUERY in a['href']:
                url = BASE_URL + a['href']
                logger.write(f"Match found: {url}\n")
                return url

    except Exception as e:
        print("Error while scraping:", e)
    finally:
        logger.close()
        driver.quit()

def get_advent_of_code():
    EST = pytz.timezone('US/Eastern')
    month = datetime.now(EST).month
    year = datetime.now(EST).year
    day = datetime.now(EST).day
    url = f'https://adventofcode.com/{year}/day/{day}'
    if month == 12:
        return url
    else:
        raise Exception(f"{PROG_NAME} - It is not December, so this function should not be called.")
