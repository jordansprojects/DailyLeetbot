import dailyLeetCodeProblem as dlcp
from datetime import datetime # kinda weird but the way it is 
import pytz # for timezone  conversion

# tests dailyLeetCodeProblem functionality


EST = pytz.timezone('US/Eastern') # Advent of Code timezone
UTC = pytz.utc                   # Leetcode Daily challenge timezone

leet =dlcp.get_daily_challenge()
if ( not leet):
    print("Test 1 FAIL. The daily challenge should not be null.")
else:
    print("Test 1 PASS. The daily challenge is at least not null.\nVerify whether the URL is correct : " + leet) 

if (datetime.now(EST).month != 12):
        print("It is not December, so an exception should be raised and then handled...")
        try:
            advent = dlcp.get_advent_of_code()
        except Exception as e:
            print(f"Test 2 PASS : Exception Caught= {e}")
            exit(0)

        print("Test 2 FAIL. The advent of code should throw an exception because it is not december EST.")
else:
    print("It is December (EST) , so the exception should not be thrown and a valid link should be retrieved...")
    try:
        advent = dlcp.get_advent_of_code()
    except:
        print("Test 2 FAIL. It is December EST, an advent of code link should be retrievable for today.")
    print("Test 2 PASS. The advent of code function was able to retrieve a link" + advent)

