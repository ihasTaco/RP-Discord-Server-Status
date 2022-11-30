# RP-Discord-Server-Status
An Open-Source Server Status Discord Bot

This is an Open Source Discord Bot, made in Discord.py to query game servers!

This bot is primarily going to be used for the <a href="https://discord.gg/royal-productions-360541835371741185">Royal Productions</a> Discord server, but I thought there wasn't enough Open Source query bots available, and since my favorite bot 'Game Status' has switched teams and put up a paywall for more then 5 servers (we have 9) I thought it would be a good idea to make one instead!

This is my first try with python and I'm still learning the ropes, so bear with me.

# What does this bot do?
In it's current state:
- It uses a mariaDB database to hold server information (will probably add mySQL support later)
- once the bot has gotten all the information from the database, it will use a2s to query servers
- finally, it will take all the information, and embed it in a discord embed message and send it to the channel of your choosing (Discord Channel ID's are held in the DB)
- The bot automatically sizes servers array, so you can use servers[row_index][column_index] to get the required information!
- Fixed the issue where the bot crashes on server being down.
- There is now a config, so no need to mess with bot.py code*
- The bot automatically refreshes the embeds! (Default is 60 seconds, you can change this in the config!)
- the bot now has the ability to edit messages, so no more deleting old embeds!

# What needs some work?
- The code is kinda messy as I coded this in less then 4 hours, so code cleanup

# What's next?
This is only for Source Queries, Minecraft is not included! I will work on this at some point!

I want to add player graphs, I think I can use MatPlotLib to acheive this, but I don't how to store the player info. I don't want to store it in the database, as I would like to keep that as clean as possible, but I think that may be my only option...

## Supported Games

While this *should* support all Source Games, I have tested these:

AppID | Game | Works | Notes
----- | ---- | :---: | ----
162107 | [DeadPoly](https://store.steampowered.com/app/1621070/) | :white_check_mark: |
304930 | [Unturned](https://store.steampowered.com/app/304930/) | :white_check_mark: |
251570 | [7 Days to Die](http://store.steampowered.com/app/251570) | :white_check_mark: |
252490 | [Rust](http://store.steampowered.com/app/252490/) | :white_check_mark: |
~ | [Minecraft](http://www.minecraft.net/) | :x: |


# How to use this
I am not providing hosting! So you will need to, <a href="https://discordpy.readthedocs.io/en/stable/discord.html">Set up</a> a <a href="https://discord.com/developers/applications">Bot Application on Discord</a> and make sure you have MESSAGE CONTENT INTENT enabled under bots

This bot is using:<br>
<a href="https://github.com/Yepoleb/python-a2s">python-a2s</a> - pip3 install python-a2s<br>
<a href="https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/">mariaDB</a> - pip3 install mariadb

All information is held in a localhost database (you can edit the database ip, port, username, password in `config.py`, so all you really need to do is add the correct information into the database and run the script with `python bot.py` and your done!

If you use anything in my script, give me credit i guess, i don't care...
