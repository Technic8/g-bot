# G-Bot

This is my personal ongoing Discord chatbot project, which I have been working on since September of 2023.
There is nothing particularly special about this bot (at the moment), it has several general purpose features such as greeting members as they join, as well as some academic features such as a course lookup command and a final grade calculator.

I will post any updates to the source code to this repo when they are ready to be shared. <br>
<br>

A few notes:
- The mashup command works by determining if 2 emojis are combineable through checking a text file of emoji mashup urls. The emojiurls.txt file was retrieved from a gist made by Ryan Seddon: https://gist.github.com/ryanseddon/0925ba915d4f865228ee3e6e0ddbe52c
- G-Bot has nothing affiliated with any company. I called it G-bot just cause.<br>


## Commands
- `!help`       Gives you information about a command presented by the user.
- `!magic8ball` Gives you a random answer to any prompt.
- `!mashup`     Combines 2 emojis into one new emoji using Google's Emoji Kitchen.
- `!rate`       Rates anything on a scale from 1 to 10.
- `!wanted`     Puts any user's pfp onto a wanted poster.
- `!finalgrade` Prompts the user for their current grade for a course, their desired grade from that course, and the final weight to give a final exam grade prediction for them.
