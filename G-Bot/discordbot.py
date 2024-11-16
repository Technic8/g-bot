# Import Discord
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

# Import Pillow
from PIL import Image
from io import BytesIO

# Gets the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) # Sets command prefix    

# Other modules

import random
import pandas
import asyncio
import math
import time

chaos_mode = False

# Confirmation that bot is online
@bot.event
async def on_ready():
    print(f"{bot.user} has successfully logged in!")

# Bot will say hello when a member joins the server
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1144988260561592401)
    await channel.send(f"Greetings {member.mention}, and welcome to the GMU CEC server! While you are brand new to this server: \n\
- 🗒️ Read the rules and get access to the server in <#1148481854387802112> \n\
- <:dogSerious:1203543332580761630> Get your essential roles in <#1148482425161265243> and <#1149178608095604827> \n\
- <:zssf:1220525056069730446> Grab your course roles in <#1250247926463336552>, <#1250278132037062688>, <#1250277994669281284>, and <#1250252019353260124> \n\
- 👋 Say hello in <#1144988260561592404>!")

# Bot will say goodbye when a member joins the server
@bot.event
async def on_member_remove(self, member):
    channel = bot.get_channel(1144988260561592401)
    await channel.send(f"Farewell, @{member.mention}.")

@bot.event
async def on_message(message):
    global chaos_mode
    # Check if the message author is not the bot
    if message.author == bot.user:
        return
    
    # React with "ok" whenever someone says ok
    if "ok" in message.content:
        if message.guild.id == 1144988260100214894 or message.guild.id == 771106101445525514:
            if chaos_mode:
            
                emoji = "\N{SQUARED OK}"
                await message.add_reaction(emoji)
    
    # Awarepine moment
    if "awarepine" in message.content or "Awarepine" in message.content:
        if message.guild.id == 1144988260100214894 or message.guild.id == 771106101445525514:
            if chaos_mode:
                await message.channel.send("Hey there! I am using Whatsapp.")
    
    # Embarass people who use gen alpha slang
    brainrot_list = ["skibbidi", "skibidi", "mew", "fanum", "gyat", "sigma", "mewing", "rizz", "ohio", "sigma", "simp", "edging", "gooning", "grimace", "sussy", "baka", "imposter", "hawk tuah"]
    for word in message.content.split():
         if word.lower() in brainrot_list:
            if message.guild.id in [1144988260100214894, 771106101445525514]:
                await message.channel.send("https://tenor.com/view/thanos-gen-alpha-compelling-argu-higher-gif-7057155085629271523", reference=message)
            break


    await bot.process_commands(message)

# !repeat command, repeats whatever message you give the bot, use quotations for a longer message
@bot.command(brief="Makes the bot repeat your message.", description="Makes the bot repeat your message. \n Usage: !repeat <message>")
async def repeat(ctx, *words):
    message = ""
    for word in words:
        message += (str(word) + " ")
    await ctx.send(message)


# !vodkatype command, messes up whatever message you give the bot
@bot.command(brief="Turn your message into something that 210Vodka would type.", description="Turn your message into something that 210Vodka would type. \n Usage: !vodkatype <message>")
async def vodkatype(ctx, *words):
    message = ""
    for word in words:
        new_word_list = []
        if len(word) > 1:
            # Multi-letter words
            n1 = random.randint(0, len(word) - 2)
            n2 = n1 + 1
            for i in range(0, len(word)):
                if i == n1:
                    new_word_list.append(word[n2])
                elif i == n2:
                    new_word_list.append(word[n1])
                else:
                    new_word_list.append(word[i])
            new_word = "".join(new_word_list)
            message += (new_word + " ")
        else:
            # One letter words
            message += (word + " ")
    await ctx.send(message)


# !wanted command, makes a specified user be put on a wanted poster
@bot.command(brief="Puts any user's pfp onto a wanted poster.", description="Puts any user's pfp onto a wanted poster. \n Usage: !wanted <user> Note: If no user is given, GBot will use the pfp of the user who called it")

async def wanted(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author # Sets user to yourself if no user is given
    
    wanted = Image.open("wanted.jpg")

    # Gets the user's profile picture
    data = BytesIO(await user.display_avatar.read())
    pfp = Image.open(data)
    
    pfp = pfp.resize((532, 532))
    wanted.paste(pfp, (101, 334))

    wanted.save("profile.jpg")

    await ctx.reply(file=discord.File("profile.jpg"))

@bot.command(brief="Combines 2 emojis into one new emoji using Google's Emoji Kitchen.", description="Combines 2 emojis into one new emoji using Google's Emoji Kitchen. \n Usage: !mashup <emoji1> <emoji2> Note: Using a single emoji will make the command combine the emoji with itself. Keep in mind that not all emojis are available for mashups, for the time being.")

async def mashup(ctx, emojis=""):
    """Combines 2 emojis into one new emoji using Google's Emoji Kitchen."""

    textfile = open("emojiurls.txt", "r")
    emoji_links = textfile.readlines()

    emoji1 = ""
    emoji2 = ""

    sent = False

    emoji1 = emojis[0]
    emoji2 = ""

    if len(emojis) == 1:
        emoji2 = emojis[0]
    else:
        emoji2 = emojis[-1]


    emoji1 = f"{ord(emoji1):X}".lower()
    emoji2 = f"{ord(emoji2):X}".lower()

    for link in emoji_links:
        combo_1 = "u" + emoji1 + "_" + "u" + emoji2
        combo_2 = "u" + emoji2 + "_" + "u" + emoji1
        if combo_1 in link:
            await ctx.send(link)
            sent = True
            break
        elif combo_2 in link:
            await ctx.send(link)
            sent = True
            break
    if not sent:
        await ctx.send("Error. Please try again. You need 1-2 DEFAULT discord emojis to make this work. Please note that not all emojis are supported. Usage: `!mashup <emoji1> <emoji2>`")

@bot.command(brief="Ask Talking Ben anything!", description="Ask Talking Ben anything! \n Usage: !talkingben <question \(optional\)>")
async def talkingben(ctx):
    num = random.randint(0, 6)
    
    gifs = {
    0: "https://tenor.com/view/ben-yes-yes-fthememer-phone-call-yes-call-yes-gif-24938145",
    1: "https://tenor.com/view/dog-saying-no-no-ben-no-phone-call-no-call-no-gif-24938149",
    2: "https://tenor.com/view/talking-ben-talking-yes-yess-talking-ben-yes-gif-25277067",
    3: "https://tenor.com/view/hohho-ho-gif-24966256",
    4: "https://tenor.com/view/talking-ben-ugh-gif-25061556",
    5: "https://tenor.com/view/talking-ben-phone-hang-up-gif-25061552",  
    6: "https://tenor.com/view/talking-ben-talking-scared-talking-ben-scared-fall-gif-25277065"
    }

    await ctx.send(gifs[num])

# !uwuify command, turns your message into an abominition
@bot.command(brief="Turns your message into an abomination.", description="Turns your message into an abomination. \n Usage: !uwuify <message>")
async def uwuify(ctx, *words):
    msg = ""
    for word in words:
        msg += (str(word) + " ")
    msg = msg.replace("o", "u")
    msg = msg.replace("O", "U")
    msg = msg.replace("r", "w")
    msg = msg.replace("R", "W")
    msg = msg.replace("l", "w")
    msg = msg.replace("L", "W")

    await ctx.send(msg)

# !rate command
@bot.command(brief="Rates anything on a scale from 1 to 10.", description="Rates anything on a scale from 1 to 10. \n Usage: !rate <topic>")
async def rate(ctx, *words):
    thing = ""
    for word in words:
        if words.index(word) != len(words) - 1:
            thing += (str(word) + " ")
        else:
            thing += str(word)
    num = random.randint(0, 10)
    await ctx.send(f"I'd give {thing} a {num} out of 10.")


@bot.command(brief="Turns chaos mode on or off.", description="Turns chaos mode on or off. \n Usage: !chaosmode <on/off>")
async def chaosmode(ctx, toggle):
    global chaos_mode
    if toggle == "on":
        if chaos_mode == False:
            await ctx.send("You have been warned...")
            chaos_mode = True
        else:
            await ctx.send("The chaos is already around us.")
        
    elif toggle == "off":
        if chaos_mode == True:
            chaos_mode = False
            await ctx.send("The chaos dawns, but it never will disappear...")
        else:
            await ctx.send("It is seemingly peaceful, actually.")
    else:
        await ctx.send("Error: Please try again. Make sure you're using \'on\' or \'off.\'")

# ! Magic 8ball command
@bot.command(brief="Gives you a random answer to any prompt", description="Gives you a random answer to any prompt. \n Usage: !magic8ball <prompt \(optional\)>")
async def magic8ball(ctx):
    num = random.randint(0, 10)
    messages = {
        # "Yes" Answers:

        1: "Without doubt.",
        2: "Answer: Yes. Source: ChatGPT.",
        3: "You bet.",
        4: "Uh huh.",
        5: "YEAHHHHHH",
        6: "Outlook looking good.",
        7: "Certainly.",
        8: "Absolutely. Your life depends on it.",
        9: "Mom says yes, so yes",
        10: "Definitely.",

        # "Maybe" Answers:
        11: "Hmmmm...",
        12: "Come back in a few minutes and I should have the answer ready.",
        13: "You probably shouldn't be asking a discord bot this question.",
        14: "Do a Google search.",
        15: "Want to buy DLC: --Get Answer-- ?",
        16: "Maybe?",
        17: "Go ask mom. She knows best.",
        18: "I think you already know what the answer is.",
        19: "404 - ANSWER NOT FOUND",
        20: "Not even I know the answer to this question.",

        # "No" Answers:

        21: "NOPE",
        22: "Answer: No. Source: I made it up.",
        23: "Probability of this happening: 0 Game over. Play again?",
        24: "Mom says no",
        25: "Odds of this happening are just like the odds of an elephant to teleport right behind you.",
        26: "Only once the gods intervene",
        27: "IMPOSSIBRU!!",
        28: "Once in a blue moon.",
        29: "Yeah, nah",
        30: "Outlook not looking so good."
    }       

    await ctx.send(messages[num])

@bot.command(brief="Gives you a final score needed to achieve a certain grade from a course.", description="Gives you a final score needed to achieve a certain grade from a course. \n Usage: !finalgrade")
async def finalgrade(ctx):
    calculator_contents = []

    prompts = [
        "Please enter your current grade (0-100 grading scale) in your course.",
        "Please enter the grade you want to achieve (0-100 grading scale) from this course.",
        "Please enter the weight of the final (0-100%)."
    ]

    passed_arg = False
    cancelled = False
    for i in range(len(prompts)):
        if not cancelled:
            await ctx.send(f"{ctx.author.mention} {prompts[i]} Type \"cancel\" at any time to cancel this command.")
            passed_arg = False
            while not passed_arg:
                try:
                    arg = await bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=60.0)
                    arg = arg.content
                    if arg == "cancel":
                        await ctx.send("Command cancelled by user.")
                        cancelled = True
                        break
                    try:
                        calculator_contents.append(float(arg))
                    except ValueError:
                        await ctx.send("Invalid argument, please try again.")
                    passed_arg = True
                except asyncio.TimeoutError:
                    await ctx.send("Command cancelled due to user inaction.")
                    cancelled = True
                    break

    ez_final_messages = [
        "We chillin' with this one!",
        "Don't bother studying.",
        "Honestly, don't panic. You're in a really good place!",
        "You got this easy.",
        "You could probably sleepwalk through this final.",
        "I mean COME ON! You could take this exam blindfolded and still pass your class. Bruh!"
    ]

    grindtime_final_messages = [
        "Get to it then!",
        "Gotta lock in for this one...",
        "It's grind time, boys.",
        "Throw away your phone, you won't need it.",
        "Night time study session, anyone?",
        "With great preparation, you can achieve this.",
        "GL, m8.",
        "You got this."
    ]

    cooked_final_messages = [
        "Idk m8, you seem cooked for this final.",
        "Think realistically, could you settle with a lower grade from this course?",
        "Honestly, no one's gonna ask you about how you did on your final 30 years from now, right?",
        "WE RETAKIN THE COURSE WITH THIS ONE 🗣️🔥🔥🔥",
        "Not even Gongaga can save you here...",
        "Perhaps build a time machine instead?"
    ]
    
    
    if len(calculator_contents) == 3:
        current_grade = calculator_contents[0]
        desired_grade = calculator_contents[1]
        final_weight = calculator_contents[2]
        if (current_grade >= 0 and current_grade <= 120) and (desired_grade >= 0 and desired_grade <= 120) and (final_weight > 0 and final_weight <= 100):

            final_grade = (desired_grade - current_grade * (1 - (final_weight/100))) / (final_weight/100)
            final_grade = round(final_grade, 2)


            msg = ""
            if final_grade > 100:
                msg = cooked_final_messages[random.randint(0, len(cooked_final_messages))]
            elif final_grade > 50:
                msg = grindtime_final_messages[random.randint(0, len(grindtime_final_messages))]
            else:
                msg = ez_final_messages[random.randint(0, len(ez_final_messages))]
            
            await ctx.send(f"You need a {final_grade} on your final to get a {desired_grade} in your class. {msg}")

        else:
            await ctx.send("https://tenor.com/view/thanos-impossible-cant-believe-gif-14748764")

bot.run(TOKEN)
