# finds the daily leetcode problem
import requests
import bs4
from datetime import datetime
import pytz # timezone conversions
import sys


def get_daily_challenge():
    logger = open ('logs/dlcp.log', 'w')
    # our link will contain this data
    query_str =  '?envType=daily-question&envId=' + datetime.now(pytz.utc).strftime('%Y-%m-%d') # leetcode uses UTC
    logger.write(sys.argv[0] + " Using query string " + query_str + '\n')
    url_to_scrape = 'https://leetcode.com/problemset/all/' 
    response = requests.get(url_to_scrape)
      
    # url we will append to once we find the daily question element
    base_url = 'https://leetcode.com'
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
        raise Exception("dailyLeetCodeProblem.py : It is not December so this function should not be called.")
        
