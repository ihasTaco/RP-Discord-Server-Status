# This bot is now marked depricated
If you still want to use an open source, fully customizable server status but, [check my new bot out!](https://github.com/ihasTaco/ServerQuery

# RP-Discord-Server-Status

Server Status is an open-source Discord bot that allows users to quickly and easily view the status of their Source and Minecraft game servers. With customizable settings and live updates, this bot makes it easy for users to monitor the performance and activity levels of their servers in real-time. Created by Royal Productions, this bot is free to use and can be modified to fit the unique needs of any server.

Here are some features that this bot offers!
 - Offers users a high degree of configurability, giving them the ability to tailor the bot's behavior and performance to their specific requirements and preferences.
 - Enables users to make live changes to the bot's configuration without interrupting its operation, making it easier for users to adjust the bot's settings and performance on the fly.
 - Retrieves data about the server's name, map, game mode, and current players, providing users with essential information about the server's current state and activity levels.
 - Displays the server's name, map, game mode, and current players, providing users with essential information about the server's status and activity levels.
 - Provides an up-to-date list of the players in the server, giving users valuable information about the server's population and activity levels.
 - Provides an easy-to-understand graph that shows the number of players on the server over time, helping users understand the server's peak and off-peak times.
 - Enables users to set the frequency of server updates, allowing them to determine how often the bot checks the server's status and activity levels.

[Supported Game Servers](https://github.com/ihasTaco/RP-Discord-Server-Status#supported-games)<br>
[Bot Showcase](https://github.com/ihasTaco/RP-Discord-Server-Status#bot-showcase)

## Getting Started
### Prerequisites
Install Python 3.9 or later if it is not already installed on your system. You can download and install Python from the [official Python website](https://www.python.org/downloads/).

Create a new Discord bot by following the instructions on the [Discord Developer Portal](https://discord.com/developers/docs/intro). You will need to create/log into a Discord account and create a new application on the Developer Portal to create your bot.

### Installing the Bot

Install the required packages for your bot by running the following command in a terminal or command prompt: ```pip install -r requirements.txt``` This will install all of the required packages for your bot, including discord.py, python-a2s, mcstatus, mariaDB, matplotlib and numpy.

Download the source code for your bot from GitHub using your perfered method and extract it to a new directory on your system (perferably somewhere easy to access).

Open the config.py file in a text editor and enter the required information for your bot, including the bot's token, database information, and customize the bot with all the available settings (don't worry these are all extremely documented)

### Running the Bot

Use: ```cd path/to/your/bot``` to point your terminal or command prompt to the correct location
Run your bot by running the bot.py file in a terminal or command prompt using the following command: ```python bot.py``` This will start your bot and connect it to the Discord API, allowing users to see your sexy new Server Status bot.

[Invite your bot](https://discordpy.readthedocs.io/en/stable/discord.html) to your Discord server by following the instructions on the Discord Developer Portal. Once your bot is added to your server, users will be able to see your servers information in real time.

To manage servers with your bot, you can use the built in commands: ```/serveradd, /serverdel, & /serverlist ``` or you can manage them in the database!

And thats it easy as that, your done!

### Optional Tools
While these aren't necessary, they are highly recommended!<br>
[Xampp](https://www.apachefriends.org/) - (This is a required tool but you have options!) Used for database (Alternatively, you can also use, [WampServer](https://www.wampserver.com/en/), and other alternatives)<br>
[HeidiSQL](https://www.heidisql.com/) - For accessing database, you could use phpmysql, but heidi is easier to use.<br>

## Command Usage
There are some new commands that I would like to bring attention to, that wasn't in the original plan!<br>
Added 3 new commands to the bot: /serveradd, /serverdel, and /serverlist

```/serveradd``` - this will take in 7 arguments ip, port, query port, game name, server name, channel ID, and the location.
I will explain some not so obvious arguments here:
 - Game Name - This is what will be displayed in the 'Game' field in the embed.
 - Server Name - While similar to the Game Name, This will be displayed as the embed title, IF you chose to enable that setting.
 - Channel ID - Where the embed will be sent to.
 - Location - This can be whatever, but default is an emoji flag and 2 letter country code (i.e. :flag_us: US)

```/serverdel``` - This will take 1 argument, DB Index<br>
When the server is deleted from the database the ID will automatically be reset to 0 so any new servers will be added to the next available ID

```/serverlist``` - this takes no arguments, but will list out all of the servers in the database.<br>
It will display this information for each server:
 - DB Index - This is the index in the database that you can use to delete a server
 - Server Name - NOT the game name, as hopefully, the server name will be a little more detailed than the game name.
 - Connection - This will show the IP:Port of the server for extra clarification on which server is which.

# Supported Games

While this *should* support all Source Games, I have tested these:
If you use this and test it on other servers, Fork this and submit a Pull Request with updated information!

AppID | Game | Works 
----- | ---- | :---: 
10 | [Counter Strike](http://store.steampowered.com/app/10/) | :white_check_mark: |
440 | [Team Fortress](http://store.steampowered.com/app/440/) | :white_check_mark: |
730 | [CS:GO](http://store.steampowered.com/app/730/) | :white_check_mark: |
107410 | [Arma 3](http://store.steampowered.com/app/107410/) | :white_check_mark: |
162107 | [DeadPoly](https://store.steampowered.com/app/1621070/) | :white_check_mark: |
304930 | [Unturned](https://store.steampowered.com/app/304930/) | :white_check_mark: |
251570 | [7 Days to Die](http://store.steampowered.com/app/251570) | :white_check_mark: |
252490 | [Rust](http://store.steampowered.com/app/252490/) | :white_check_mark: |
346110 | [Ark: Survival Evolved](http://store.steampowered.com/app/252490/) | :white_check_mark: |
~ | [Minecraft](http://www.minecraft.net/) | :white_check_mark: |

# Bot Showcase
<img src="https://media.discordapp.net/attachments/1046993037240303728/1050509951325458482/Screenshot_2022-12-08_132930.png" style="width: 250px">
<img src="https://media.discordapp.net/attachments/1046993037240303728/1050509951690354718/Screenshot_2022-12-08_133027.png" style="width: 250px">
<img src="https://media.discordapp.net/attachments/1046993037240303728/1050509952055267418/Screenshot_2022-12-08_133103.png" style="width: 250px">
<img src="https://media.discordapp.net/attachments/1046993056227930173/1050982150792548352/Commands.png" style="width: 250px">
<img src="https://media.discordapp.net/attachments/1046993056227930173/1050982189099130920/serverlist_screenshot.png" style="width: 250px">

If you use anything in my script, give me credit I guess, I don't care...
