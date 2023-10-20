import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

#Gets the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #Sets command prefix    

#Other modules

import random
import math

#Confirmation that bot is online
@bot.event
async def on_ready():
    print(f"{bot.user} has successfully logged in!")


# Bot will say good morning to you if you say good morning in the chat
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == "good morning" or message.content == "gm" or message.content == "Good morning":
        await message.channel.send("Good morning.")
    
    await bot.process_commands(message)

# !repeat command, repeats whatever message you give the bot, use quotations for a longer message
@bot.command()
async def repeat(ctx, msg):
    message = str(msg)
    await ctx.send(message)

# !add command, adds 2 numbers given by user
@bot.command()
async def add(ctx, num1, num2):
    result = float(num1) + float(num2)
    await ctx.send(result)


# !talkingben command, returns a random talking ben gif
@bot.command()
async def talkingben(ctx):
    num = random.randint(0, 5)

    gifs = {
    1: "https://tenor.com/view/talking-ben-yes-gif-27130395",
    2: "https://tenor.com/view/talking-ben-talking-talking-ben-no-gif-25277070",
    3: "https://tenor.com/view/hohho-ho-gif-24966256",
    4: "https://tenor.com/view/talking-ben-ugh-gif-25061556",
    5: "https://tenor.com/view/talking-ben-phone-hang-up-gif-25061552"   
    }

    await ctx.send(gifs[num])

# !uwuify command, turns your message into an abominition
@bot.command()
async def uwuify(ctx, msg):
    msg = msg.replace("o", "u")
    msg = msg.replace("O", "U")
    msg = msg.replace("r", "w")
    msg = msg.replace("R", "W")

    await ctx.send(msg)





bot.run(TOKEN)