# finds the daily leetcode problem
import requests
import bs4
from datetime import datetime
import pytz # timezone conversions
import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Scrapes leetcode problemset page for the daily question so the link can be retrieved and posted by the bot
# This is a Wonderful resource on selenium for web scraping purposes :
#    https://www.browserstack.com/guide/web-scraping-using-selenium-python
def get_daily_challenge():
    WAIT_TIME = 6000
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("--disable-dev-shm-usage");
    chrome_options.add_argument("--disable-renderer-backgrounding");
    chrome_options.add_argument("--disable-background-timer-throttling");
    chrome_options.add_argument("--disable-backgrounding-occluded-windows");
    chrome_options.add_argument("--disable-client-side-phishing-detection");
    chrome_options.add_argument("--disable-crash-reporter");
    chrome_options.add_argument("--disable-oopr-debug-crash-dump");
    chrome_options.add_argument("--no-crash-upload");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--disable-low-res-tiling");
    chrome_options.add_argument("--log-level=3");
    chrome_options.add_argument("--silent");
    driver=webdriver.Chrome(options=chrome_options)
    logger = open ('logs/dlcp.log', 'w')
    # our link will contain this data
    query_str =  'envType=daily-question&envId=' + datetime.now(pytz.utc).strftime('%Y-%m-%d') # leetcode uses UTC
    logger.write(sys.argv[0] + " Using query string " + query_str + '\n')
    url_to_scrape = 'https://leetcode.com/problemset/' 
    response = requests.get(url_to_scrape)
    
    # url we will append to once we find the daily question element
    base_url = 'https://leetcode.com'
    wait = WebDriverWait(driver, WAIT_TIME)
    driver.get(url_to_scrape)
    get_url = driver.current_url
    wait.until(EC.url_to_be(url_to_scrape))
    if(get_url != url_to_scrape):
        raise Exception(sys.argv[0] + "URL does not match.\nExpected : " + url_to_scrape + "\nActual: " + get_url )

    page_source = driver.page_source
    # logger.write(str(page_source))
    # driver.quit()
    soup = bs4.BeautifulSoup(page_source, features="html.parser")
    for a in soup.body.find_all('a', href=True):
        #logger.write("url contained " + match['href'] + '\n')
        if(query_str in a['href']):
            url = base_url + a['href']
            logger.write("match found : " + a['href'])
            return url



   
    
    logger.close()

def get_advent_of_code():
    EST = pytz.timezone('US/Eastern') # advent of code uses EST
    month = datetime.now(EST).month # change these values to a valid number if you want to debug
    year = datetime.now(EST).year
    day = datetime.now(EST).day
    url = 'https://adventofcode.com/' + str(year) + '/day/'+ str(day)
    if month == 12:
        return url
    else:
        raise Exception(sys.argv[0] + " It is not December so this function should not be called.")
            
