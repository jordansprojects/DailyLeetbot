import discord
import asyncio
from datetime import datetime
from discord.ext import commands, tasks
import pytz
#TO-DO rewrite target channel as a data member 

import dailyLeetCodeProblem as dlcp
TARGET_CHANNEL_NAME =  "programming"
XMAS_EMOJIS1 = " :christmas_tree: :santa: :snowman2: "
XMAS_EMOJIS2 = " :snowman2: :santa: :christmas_tree: "
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
            await self.target_channel.send("Hello. I am here to post the leetcode question of the day.")
            self.post_daily_question.start()
        else:
            raise Exception("leetbot.py : target channel not set.")

    @tasks.loop(hours=24)
    async def post_daily_question(self):
        month = datetime.now().month
        if self.target_channel:
            await self.target_channel.send("Challenge of the day :blush:  " + dlcp.get_daily_challenge() )
        if month == 12 :
            await self.target_channel.send(XMAS_EMOJIS1 +  "Ho ho ho! Advent of code challenge of the day : " + dlcp.get_advent_of_code()
                                           + XMAS_EMOJIS2)






