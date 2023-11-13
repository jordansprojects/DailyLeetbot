# finds the daily leetcode problem
import requests
import bs4
from datetime import datetime

def get_daily_challenge():
    try:
        # our link will contain this data
        query_str =  'daily-question&envId=' + datetime.now().strftime('%Y-%m-%d')
        url_to_scrape = 'https://leetcode.com/problemset/all/' 
        response = requests.get(url_to_scrape)
      
        # url we will append to once we find the daily question element
        base_url = 'https://leetcode.com'

        # check if request was successful
        if response.status_code == 200:
            # parse html 
            soup = bs4.BeautifulSoup(response.text, 'html.parser')

            challenge_elem = soup.find('a', href=lambda href: href and query_str in href)

            desired_url = base_url + challenge_elem['href']
            
            return desired_url
        else:
            raise Exception ("dailyLeetCodeProblem.py : request failed ")
    except Exception as e :
        print("dailyLeetCodeProblem.py: ", end="")
        print(e)


def get_advent_of_code():
    month = datetime.now().month # change these values to a valid number to debug
    year = datetime.now().year
    day = datetime.now().day
    url = 'https://adventofcode.com/' + str(year) + '/day/'+ str(day)
    if month == 12:
        return url
    else:
        raise Exception("dailyLeetCodeProblem.py : It is not December so this function should not be called.")
        
