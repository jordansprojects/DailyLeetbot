import leetbot as lb
import discord
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('token', nargs='?', help='Discord bot token. After running setup once,  .botenv file will be generated and contain your token. Use this flag to overrwite the token. https://discordgsm.com/guide/how-to-get-a-discord-bot-token ')
args = parser.parse_args();

token = None
f = open(".botenv", "w+")

#if(argparse["token"]):
    #token = argparse['token']

if(token == None):
    token = input("Enter token:")
    f.write(token)

# specify intents 
intents = discord.Intents.default()
intents.message_content = True

client = lb.DailyLeetClient(intents=intents, command_prefix = '!')

try:
    client.run(token)

except Exception as e :
        print("setup.py : ", end="")
        print(e)
