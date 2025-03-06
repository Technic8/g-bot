#---------------------------------------
#               BOT SETUP
#---------------------------------------

# Import Discord

import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

# Import Pillow
from PIL import Image
from io import BytesIO

# Import BeautifulSoup
import requests
from bs4 import BeautifulSoup


# Gets the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) # Sets command prefix    

# Other modules

import random
import asyncio
import numpy

# Basic Definitions

server_ids = [
    1144988260100214894, # GMU CEC Server
    771106101445525514 # Personal Server for Testing
]


chaos_mode = False




# ---------------------------------------------------
# Member-welcoming/farewelling
# ---------------------------------------------------

welcome_channel = 1144988260561592401

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(welcome_channel)
    starter_channels = {
        "rules": 1332797657747296256,

        "self-roles": 1148482425161265243,
        "color-roles": 1149178608095604827,

        "cs-roles": 1250247926463336552,
        "swe-roles": 1292015901499068481,
        "ece-roles": 1250252019353260124,
        "meche-roles": 1250277994669281284,
        "stat-roles": 1291946284680347648,
        "math-science-roles": 1250278132037062688,

        "general": 1335206125485691002
    }

    await channel.send(f"Greetings {member.mention}, and welcome to the GMU CEC server! While you are brand new to this server: \n\
- 🗒️ Read the rules and get access to the server in <#{starter_channels['rules']}> \n\
- <:dogSerious:1203543332580761630> Get your essential roles in <#{starter_channels['self-roles']}> and <#{starter_channels['color-roles']}> \n\
- <:zssf:1220525056069730446> Grab your course roles in <#{starter_channels['cs-roles']}>, <#{starter_channels['swe-roles']}>, <#{starter_channels['ece-roles']}>, <#{starter_channels['meche-roles']}>, \
<#{starter_channels['stat-roles']}>, and <#{starter_channels['math-science-roles']}> \n\
- 👋 Say hello in <#{starter_channels['general']}>!")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(welcome_channel)
    await channel.send(f"Farewell, {member.mention}.🫡")



# ------------------------------------------
# ACADEMIC COMMANDS
# ------------------------------------------

class Academic(commands.Cog):

    # ----------------------------------------------------------
    # !info command, gives you information about any GMU course.
    # ----------------------------------------------------------
    
    @commands.command(name="info", brief="Gives you basic information about any GMU course.", description="Gives you basic information about any GMU course (ex: credits, description, prerequisites, schedule type). \n Usage: !info <major> <num>")
    async def info(self, ctx, major_id, course_num):
        full_desc = ""
        course_found = True
        data = []
        url = "https://catalog.gmu.edu/courses/" + major_id.lower() + "/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        if soup.title.text == "404 Page Not Found":
            course_found = False
        else:
            all_courses = soup.find_all("div", class_="courseblock")
            for course in all_courses:
                item = {}

                item["Course ID"] = major_id.upper() + " " + course.find("strong", class_="cb_code").text[-4:-1]
                item["Course Name"] = course.find("em", class_="cb_title").text[:-1]

                item["Credits"] = course.find("div", class_="courseblocktitle").text.split(".")[-2].strip()
                item["Credits"] = item["Credits"].split("c")[0].strip()

                # Check if the number of credits is flexible in a course

                if "-" in item["Credits"]:
                    item["Credits"] = item["Credits"].split("-")
                    item["Credits (lowest)"] = int(item["Credits"][0])
                    item["Credits (highest)"] = int(item["Credits"][-1])
                    item["Credits"] = numpy.nan
                else:
                    item["Credits"] = int(item["Credits"])
                
                item["Description"] = course.find("div", class_="courseblockdesc").text.replace("\xa0", " ")


                prereqs = course.find("p", class_="prereq")

                if prereqs != None:
                    p_courses = prereqs.find_all("a", class_="bubblelink code")
                    p_course_list = []
                    for p_course in p_courses:
                        p_course_list.append(p_course.text.replace("\xa0", " "))
                        
                        # Add course ids to every p-course

                        for i in range(len(p_course_list)):
                            if len(p_course_list[i]) > 3:
                                id = p_course_list[i][:-4]
                            else:
                                p_course_list[i] = f"{id} {p_course_list[i]}"
                        
                        # Remove duplicates
                        p_course_list = list(dict.fromkeys(p_course_list))
                    item["Prereqs"] = p_course_list
                else:
                    item["Prereqs"] = None

                item["Schedule Type"] = ""

                for i in range(len(course.find_all("div", class_="courseblockextra"))):
                    if "<strong>Schedule Type: </strong>" in str(course.find_all("div", class_="courseblockextra")[i]):
                        item["Schedule Type"] = course.find_all("div", class_="courseblockextra")[i].text.replace("Schedule Type: ", "")

                data.append(item)
        
        
        
        if course_found:
            for course in data:
                if course["Course ID"] == f"{major_id.upper()} {course_num}":
                    prereqs = ", ".join(course['Prereqs'])

                    full_desc = f"**{course['Course ID']}** - {course['Course Name']}\n\
**Credits:** {course['Credits']}\n\
*{course['Description']}* \n\
**Prerequisites** (not all may be required)**:** {prereqs} \n\
**Schedule Type:** {course['Schedule Type']}"
                
        if len(full_desc) > 0:
            await ctx.send(full_desc)
        else:
            await ctx.send("Course doesn't exist, please try again")

    # -------------------------------------------------------------------------------------
    # !finalgrade command, gives you a final score needed to achieve a certain grade.
    # -------------------------------------------------------------------------------------
    
    @commands.command(name="finalgrade", brief="Gives you a final score needed to achieve a certain grade.", description="Gives you a final score needed to achieve a certain grade from a course. \n Usage: !finalgrade. Note: You can type \"cancel\" at any time to cancel this command. It also times out after 60 seconds of inaction.")
    async def finalgrade(self, ctx):
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
                            passed_arg = True
                        except ValueError:
                            await ctx.send("Invalid argument, please try again.")
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
                    msg = cooked_final_messages[random.randint(0, len(cooked_final_messages) - 1)]
                elif final_grade > 70:
                    msg = grindtime_final_messages[random.randint(0, len(grindtime_final_messages) - 1)]
                else:
                    msg = ez_final_messages[random.randint(0, len(ez_final_messages) - 1)]
                    
                    
                await ctx.send(f"{ctx.author.mention} You need a {final_grade} on your final to get a {desired_grade} in your class. {msg}")
            else:
                await ctx.send("https://tenor.com/view/thanos-impossible-cant-believe-gif-14748764")


# --------------------------------
# FUN COMMANDS
# --------------------------------




class Fun(commands.Cog):

    # -------------------------------------------------------------------
    # !wanted command, makes a specified user be put on a wanted poster
    # -------------------------------------------------------------------

    @commands.command(brief="Puts any user's pfp onto a wanted poster.", description="Puts any user's pfp onto a wanted poster. \n Usage: !wanted <user> Note: If no user is given, GBot will use the pfp of the user who called it")

    async def wanted(self, ctx, user: discord.User = None):
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

    # ----------------------------------------------------------------------------
    # !mashup command, combines 2 emojis together using Google's Emoji Kitchen API
    # ----------------------------------------------------------------------------


    @commands.command(brief="Combines 2 emojis into one new emoji using Google's Emoji Kitchen.", description="Combines 2 emojis into one new emoji using Google's Emoji Kitchen. \n Usage: !mashup <emoji1> <emoji2> Note: Using a single emoji will make the command combine the emoji with itself. Keep in mind that not all emojis are available for mashups, for the time being.")

    async def mashup(self, ctx, emojis=""):
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



    # -------------------------------------------------------------------------------------
    # !rate command, rates anything on a scale from 1 to 10.
    # -------------------------------------------------------------------------------------


    @commands.command(brief="Rates anything on a scale from 1 to 10.", description="Rates anything on a scale from 1 to 10. \n Usage: !rate <topic>")
    async def rate(self, ctx, *words):
        thing = ""
        for word in words:
            if words.index(word) != len(words) - 1:
                thing += (str(word) + " ")
            else:
                thing += str(word)
        num = random.randint(0, 10)
        await ctx.send(f"I'd give {thing} a {num} out of 10.")


    # -------------------------------------------------------------
    # !magic8ball command, gives you a random answer to a prompt.
    # -------------------------------------------------------------

    @commands.command(brief="Gives you a random answer to any prompt", description="Gives you a random answer to any prompt. \n Usage: !magic8ball <prompt \(optional\)>")
    async def magic8ball(self, ctx):
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
        num = random.randint(0, len(messages) - 1)
        await ctx.send(messages[num])




# Run the bot

@bot.event
async def on_ready():

    await bot.add_cog(Academic())
    await bot.add_cog(Fun())

    print(f"{bot.user} has successfully logged in!")


bot.run(TOKEN)
