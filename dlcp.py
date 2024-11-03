import requests
import bs4
from datetime import datetime
import pytz  # Timezone conversions
import sys
import time
import json

PROG_NAME = sys.argv[0]

def get_daily_challenge():
    base_url = 'https://leetcode.com'
    api_endpoint = '/graphql'
    headers = {
        "Content-Type": "application/json",
        # Optionally, add an authorization header if needed
        # "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        date
        userStatus
        link
        question {
          acRate
          difficulty
          freqBar
          frontendQuestionId: questionFrontendId
          isFavor
          paidOnly: isPaidOnly
          status
          title
          titleSlug
          hasVideoSolution
          hasSolution
          topicTags {
            name
            id
            slug
          }
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        # Optionally, add an authorization header if needed
        # "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }

    # Prepare the payload with the query string
    payload = {
        "query": query
    }
    try:
        logger = open('logs/dlcp.log', 'a')
        response = requests.post((base_url + api_endpoint), json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        questionUrl = base_url + data['data']['activeDailyCodingChallengeQuestion']['link']
        logger.write(questionUrl)
        return questionUrl
    except e:
        logger.write(e)
    finally:
        logger.close()

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

get_daily_challenge()
