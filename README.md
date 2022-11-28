# RP-Server-Status
An Open-Source Server Status Discord Bot

This is an Open Source Discord Bot, made in Discord.py to query game servers!

This is my first try with python and I'm still learning the ropes, so bear with me.

# What does this bot do?
In it's current state:
- It uses a mariaDB database to hold server information (will probably add mySQL support later)
- once the bot has gotten all the information from the database, it will use a2s to query servers
- finally, it will take all the information, and embed it in a discord embed message and send it to the channel of your choosing (Discord Channel ID's are held in the DB)

# What needs some work?
- The code is kinda messy as I coded this in less then 4 hours, so code cleanup
- In the event of a server being down, the bot will crash as I have no error detection implemented
- This is only for Source Queries, Minecraft is not included!

# What's next?
I want to add player graphs, I think I can use MatPlotLib to acheive this, but I don't how to store the player info. I don't want to store it in the database, as I would like to keep that as clean as possible, but I think that may be my only option...

I want to auto update every 5(?) minutes or so, so I will need to figure out a refresh function.

Currently the bot will just create a new message, I want to just edit the last message sent by the bot.

# How to use this
This bot is using:<br>
<a href="https://github.com/Yepoleb/python-a2s">python-a2s</a> - pip3 install python-a2s<br>
<a href="https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/">mariaDB</a> - pip3 install mariadb

All information is held in a localhost database (you can change this in the script), so all you really need to do is add the correct information into the database and run the script with `python bot.py` and your done!
