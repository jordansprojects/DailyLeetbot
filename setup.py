import leetbot as lb
import discord
import os.path
import argparse
import json

ENV_FILE_NAME =  ('.botenv')
token = None
configs_ready = True
cowsay_enabled = False
target_channel_name = "programming"

parser = argparse.ArgumentParser()
parser.add_argument('set-token', nargs='?', help='Overrwite the discord bot token being used. https://discordgsm.com/guide/how-to-get-a-discord-bot-token ')
parser.add_argument('enable-cowsay', nargs='?', help='Enable cowsay. Bot posts daily question within a cowsay word bubble.')
parser.add_argument('disable-cowsay', nargs='?', help='Disable cowsay. Bot will not post question within a cowsay word bubble')
args = parser.parse_args();

try:
    fp = open(ENV_FILE_NAME, "r+")
    configs = json.load(fp)
except FileNotFoundError :
    print(".botenv file not found, creating it now...")
    configs = {}
    fp = open(ENV_FILE_NAME, "w")
    configs_ready = False

if configs_ready:
   cowsay_enabled = configs['cowsay_enabled']
   target_channel_name = configs['target_channel_name']
   token = configs['token']
else:
    configs['cowsay_enabled'] = cowsay_enabled
    configs['target_channel_name'] = target_channel_name


if(token == None):
    token = input("Enter token:")
    configs['token'] = token

fp.seek(0)
json.dump(configs, fp)

# specify intents 
intents = discord.Intents.default()
intents.message_content = True
client = lb.DailyLeetClient(intents=intents, command_prefix = '!', target_channel_name=target_channel_name, cowsay_enabled=cowsay_enabled)

try:
    client.run(token)

except Exception as e :
        print("setup.py : ", end="")
        print(e)
