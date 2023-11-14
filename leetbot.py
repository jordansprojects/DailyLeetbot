import discord
from datetime import datetime
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import dailyLeetCodeProblem as dlcp
import pytz # for timezone conversions

EST = pytz.timezone("US/Eastern")
UTC = pytz.utc

TARGET_CHANNEL_NAME =  "programming"
XMAS_EMOJIS1 = " :christmas_tree: :santa: :snowman2: "
XMAS_EMOJIS2 = " :snowman2: :santa: :christmas_tree: "

WELCOME = "Hello. I am Daily LeetCode Problem bot. I will post the Leetcode question everytime the new questions drops at 4:00PM PST (12:00AM UTC)"

class DailyLeetClient(commands.Bot):
    def find_target_channel(self):
        for server in self.guilds:
            for channel in server.channels:
                if isinstance(channel, discord.TextChannel) and channel.name == TARGET_CHANNEL_NAME:
                    return channel
    
    def __init__(self, *args, **kwargs):
        self.target_channel = None
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'leetbot.py: Logged on as {self.user}!')
        # set target channel 
        self.target_channel = self.find_target_channel();
        if self.target_channel:
            #init scheduler
            scheduler = AsyncIOScheduler()
            # add scheduler jobs
            # aws uses UTC, so the parameters are based on UTC military time 
            scheduler.add_job(self.post_daily_question,CronTrigger(hour="0",minute ="0", second="0")) # 4pm PST = 12am UTC when LeetCode problem of day changes
            scheduler.add_job(self.post_advent_of_code, CronTrigger(hour="5", minute="0", second="0"))  # 9pm PST = 12am EST = 5AM UTC  when advent of code is posted
            # start scheduler
            scheduler.start()

            await self.target_channel.send(WELCOME)
        else:
            raise Exception("leetbot.py : target channel not set.")

    async def post_daily_question(self):
        if self.target_channel:
            await self.target_channel.send("Problem of the day " + dlcp.get_daily_challenge() )
        
    async def post_advent_of_code(self):
        month = datetime.now(EST).month
        if month == 12 :
            await self.target_channel.send(XMAS_EMOJIS1 +  "Ho ho ho! Advent of code challenge of the day : " + dlcp.get_advent_of_code()
                                           + XMAS_EMOJIS2)


    




