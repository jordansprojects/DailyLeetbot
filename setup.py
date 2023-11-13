import leetbot as lb
import discord


#perm number : 34359756800

# run this script to start your bot
token = input("Enter token:")

# specify intents 
intents = discord.Intents.default()
intents.message_content = True

client = lb.DailyLeetClient(intents=intents)

try:
    client.run(token)

except Exception as e :
        print("setup.py : ", end="")
        print(e)