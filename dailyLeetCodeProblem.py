# finds the daily leetcode problem
import requests
import bs4
from datetime import datetime
import pytz # timezone conversions

def get_daily_challenge():
    try:
        # our link will contain this data
        query_str =  'daily-question&envId=' + datetime.now(pytz.utc).strftime('%Y-%m-%d') # leetcode uses UTC

        url_to_scrape = 'https://leetcode.com/problemset/all/' 
        response = requests.get(url_to_scrape)
      
        # url we will append to once we find the daily question element
        base_url = 'https://leetcode.com'

        # check if request was successful
        if response.status_code == 200:
            # parse html 
            soup = bs4.BeautifulSoup(response.text, 'html.parser')

            # find element containing the daily question marker along with todays date in UTC time
            challenge_elem = soup.find('a', href=lambda href: href and query_str in href)
            
            if( not challenge_elem):
                raise Exception("dailyLeetCodeProblem.py: element not found.")
            
            desired_url = base_url + challenge_elem['href']
            return desired_url
        else:
            raise Exception ("dailyLeetCodeProblem.py : request failed ")
    except Exception as e :
        print("dailyLeetCodeProblem.py: ", end="")
        print(e)


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
        
