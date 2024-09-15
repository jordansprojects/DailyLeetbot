import discord
from datetime import datetime
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import dlcp as dlcp
import pytz  # for timezone conversions
import traceback
import cowsay

#TODO: Fix Cowsay to look nice in discord chat box
#TODO: Retrieve daily question for all bot instances at once.
DEBUG = True

class DailyLeetClient(commands.Bot):
    EST = pytz.timezone("US/Eastern")
    UTC = pytz.utc
    XMAS_EMOJIS1 = " :christmas_tree: :santa: :snowman2: "
    XMAS_EMOJIS2 = " :snowman2: :santa: :christmas_tree: "
    WELCOME = "Hello. I will post the Leetcode question every time the new question drops at 4:00PM PST (12:00AM UTC)"
    DLCP_NULL_ERROR = "I don't feel so good. 🤢 \n Please check logs/dlcp.log "

    def __init__(self, *args, target_channel_name=None, cowsay_enabled=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = open('logs/leetbot.log', 'w')
        self.target_channel_name = target_channel_name
        self.cowsay_enabled = cowsay_enabled

    def prepare_message(self, message):
        if self.cowsay_enabled:
            message = cowsay.get_output_string('cow',message)
        return message

    async def on_ready(self):
        print(f'leetbot.py: Logged on as {self.user}!')
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.post_daily_question, CronTrigger(hour="16", minute="0", second="0"))  # 4pm PST = 12am UTC
        if DEBUG:
            scheduler.add_job(self.post_daily_question, CronTrigger(second="0"))
        scheduler.add_job(self.post_advent_of_code, CronTrigger(hour="5", minute="0", second="0", month="12"))  # 9pm PST = 12am EST = 5AM UTC
        scheduler.start()
        for server in self.guilds:
            for channel in server.channels:
                if isinstance(channel, discord.TextChannel) and channel.name == self.target_channel_name:
                    await channel.send(self.prepare_message(self.WELCOME))

    async def post_daily_question(self):
        for server in self.guilds:
            for channel in server.channels:
                if isinstance(channel, discord.TextChannel) and channel.name == self.target_channel_name:
                    challenge = dlcp.get_daily_challenge()
                    if challenge is not None:
                        await channel.send(self.prepare_message("Problem of the day " + challenge))
                    else:
                        await channel.send(self.prepare_message(self.DLCP_NULL_ERROR))

    async def post_advent_of_code(self):
        for server in self.guilds:
            for channel in server.channels:
                if isinstance(channel, discord.TextChannel) and channel.name == self.target_channel_name:
                    aoc = dlcp.get_advent_of_code()
                    if aoc is not None:
                        await channel.send(self.prepare_message(self.XMAS_EMOJIS1 + "Ho ho ho! Advent of code challenge of the day: " + aoc + self.XMAS_EMOJIS2))
                    else:
                        await channel.send(self.prepare_message(self.DLCP_NULL_ERROR))

    async def on_error(self, event_method, *args, **kwargs):
        self.logger.write(traceback.format_exc())
        self.logger.flush()
