import discord
import asyncio
from datetime import datetime
from discord.ext import commands, tasks

#TO-DO rewrite target channel as a data member 

import dailyLeetCodeProblem as dlcp
TARGET_CHANNEL_NAME =  "programming"
class DailyLeetClient(discord.Client):
    def find_target_channel(self):
        for guild in self.guilds:
            for channel in guild.channels:
                 if isinstance(channel, discord.TextChannel) and channel.name == TARGET_CHANNEL_NAME:
                    return channel
    
    async def on_ready(self):
        print(f'leetbot.py: Logged on as {self.user}!')
        target_channel = self.find_target_channel()
        if target_channel:
            await target_channel.send("Hi everyone! I am logging on to post the leetcode challenge every 24 hours. Expect a message 24 hours from now. ")

        while True:
            if target_channel:
                url = dlcp.get_daily_challenge()
                if url:
                    await target_channel.send("Daily leetcode challenge : " + url)
            await asyncio.sleep(24)
         

    
         






