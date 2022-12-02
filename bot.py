import os
import discord
from discord.utils import get
import mariadb
from datetime import datetime
import time
# For server query
import a2s
from mcstatus import JavaServer
# For Bot Config
import configparser
# To stop blocking  
import functools
import typing
import asyncio

cDebug = '\033[1;32m'
cSubTitle = '\033[0;36m'
cError = '\033[1;91m'
cSuccess = '\033[1;92m'
cNormal = '\033[0;00m'
cInfo = '\033[0;33m'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# In the future I may be able to completely get rid of the config.py
# if I decide to make a panel that will just edit the config.ini directly
# or I could make it a webserver, and host the panel ^ off localhost
# which you would be able to, access it from inside the network, or
# open ports (or rent hosting) and get a domain name to host it on

exec(open("config.py").read())
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

async def update_config():
    exec(open("config.py").read())
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')

debug = bool(config['GENERAL']['debugmode'] == 'True')

if debug == True:
    print("%s\n#######################################\n#%s           Debug Mode: On            %s#\n#######################################\n%s" %(cDebug, cNormal, cDebug, cNormal))

    
# Get information from config
dbHost = config['DATABASE']['host']
dbUser = config['DATABASE']['user']
dbPassword = config['DATABASE']['password']
dbDatabase = config['DATABASE']['database']
dbTable = config['DATABASE']['table']

embedColor = '0x' + config['GENERAL']['embedColor']
thumbnailImage = config['GENERAL']['thumbnailimage']
footerNote = config['GENERAL']['footernote']
footerImage = config['GENERAL']['footerimage']
showPlayerNamesInEmbed = bool(config['GENERAL']['showplayernamesinembed'] == 'True')
showDirectConnectInEmbed = bool(config['GENERAL']['showDirectConnectInEmbed'] == 'True')
showGameInEmbed = bool(config['GENERAL']['showGameInEmbed'] == 'True')
showMapInEmbed = bool(config['GENERAL']['showMapInEmbed'] == 'True')
showCurrentPlayersInEmbed = bool(config['GENERAL']['showCurrentPlayersInEmbed'] == 'True')
showSteamConnectionInEmbed = bool(config['GENERAL']['showSteamConnectionInEmbed'] == 'True')
useServerNameAsTitle = bool(config['GENERAL']['useservernameastitle'] == 'True')
showTimestamp = bool(config['GENERAL']['showtimestamp'] == 'True')
if thumbnailImage == '':
    thumbnailImage = None
if footerNote == '':
    footerNote = None
if footerImage == '':
    footerImage = None

if debug == True:
    print("\n---     Config Variable Initialization      ---")
    print("\n--- Database Config Variable Initialization ---")
    print("%sDatabase Host:%s %s" % (cInfo, cNormal, dbHost))
    print("%sDatabase User:%s %s" % (cInfo, cNormal, dbUser))
    print("%sDatabase Password:%s %s" % (cInfo, cNormal, dbPassword))
    print("%sDatabase Database:%s %s" % (cInfo, cNormal, dbDatabase))
    print("%sDatabase Table:%s %s" % (cInfo, cNormal, dbTable))
    print("\n--- General Config Variable Initialization ---")
    print("%sembedColor:%s %s" % (cInfo, cNormal, embedColor))
    print("%sthumbnailImage:%s %s" % (cInfo, cNormal, thumbnailImage))
    print("%sfooterNote:%s %s" % (cInfo, cNormal, footerNote))
    print("%sfooterImage:%s %s" % (cInfo, cNormal, footerImage))
    print("%sshowPlayerNamesInEmbed:%s %s" % (cInfo, cNormal, showPlayerNamesInEmbed))
    print("%sshowDirectConnectInEmbed:%s %s" % (cInfo, cNormal, showDirectConnectInEmbed))
    print("%sshowGameInEmbed:%s %s" % (cInfo, cNormal, showGameInEmbed))
    print("%sshowMapInEmbed:%s %s" % (cInfo, cNormal, showMapInEmbed))
    print("%sshowCurrentPlayersInEmbed:%s %s" % (cInfo, cNormal, showCurrentPlayersInEmbed))
    print("%sshowSteamConnectionInEmbed:%s %s" % (cInfo, cNormal, showSteamConnectionInEmbed))
    print("%suseServerNameAsTitle:%s %s" % (cInfo, cNormal, useServerNameAsTitle))
    print("%sshowTimestamp:%s %s" % (cInfo, cNormal, showTimestamp))

servers = []

# db needs to be a global variable as it needs to be accessed in multiple functions
try:
    db = mariadb.connect(
        host=dbHost,
        user=dbUser,
        password=dbPassword,
        database=dbDatabase
    )
    print("\n%sSuccessfully connected to database!%s" % (cSuccess, cNormal))
except mariadb.OperationalError:
    print("\n%sFailed to connect to database!%s" % (cError, cNormal))
    print("%sMake sure you typed in the correct information!%s" % (cError, cNormal))
    os._exit(1)


#######################################
#          SQL Server Query           #
#######################################

# to get the desired results, of getting rid of the numOfServers variable, I could do:
# 1. seperate the SQL Server Query into 2 functions,
#    1 function will be up to 'servers = [[0 for a in range(w)] for b in range(h)]'
#    and the rest will be another function
# 2. find a way to send the servers variable to the on_ready() function <- this is better imo, but this ^ is easier...
async def getDBInfo(x, a):
    if debug == True:
        if a == 1:
            print("%s\n#######################################\n#%s      Initial SQL Server Query       %s#\n#######################################%s" % (cSubTitle, cNormal, cSubTitle, cNormal))
        else:
            print("%s\n#######################################\n#%s          SQL Server Query           %s#\n#######################################%s" % (cSubTitle, cNormal, cSubTitle, cNormal))
    cursor = db.cursor()
    cursor.execute("SELECT * FROM %s" %dbTable)
    results = cursor.fetchall()

    if debug == True:
        if a == 1:
            print("%sSELECT * FROM %s%s" %(cInfo, dbTable, cNormal))
            if results == []:
                print("%sNothing is in the database!\nCheck to make sure your database is set up correctly!%s" % (cError, cNormal))
                os._exit(1)
            else:
                print("%sSuccessfully found %s rows! %s" % (cSuccess, len(results), cNormal))

    # Fill servers array with 0's to appropriate sizes
    w, h = 8, len(results)
    servers = [[0 for a in range(w)] for b in range(h)] 

    # start assigning results to servers array
    for y in results:
        z = 0
        while z <= len(y) - 1: 
            servers[y[0]][z] = y[ z ]
            z += 1

    if debug == True:
        if a != 1:
            print("%sDB Index: %s%s" % (cInfo, cNormal, x))
            print("%sGame: %s%s" % (cInfo, cNormal, servers[x][4]))
            print("%sResults: \n %s%s" %(cInfo, cNormal, servers[x]))
        
    if a == 1:
        return servers
    else: 
        await getServerInfo(servers, x)

#######################################
#    Send Message Info to Database    #
#######################################
async def sendMessageInfo(message, x):
    if debug == True:
        print("%s\n#######################################\n#%s    Send Message Info to Database    %s#\n#######################################%s" % (cSubTitle, cNormal, cSubTitle, cNormal))
    message = str(message).split()
    message = str(message[1]).split('id=')
    
    if debug == True:
        print("%sMessage ID:%s %s" % (cInfo, cNormal, message[1]))
    cursor = db.cursor()
    cursor.execute('UPDATE server_info SET messageID = \"%s\" WHERE ID = \"%s\"' % (str(message[1]), x))
    db.commit()
    if debug == True:
        print("%sMessage ID Sent to Database Successfully!%s" % (cSuccess, cNormal))
    
#######################################
#             Server Query            #
#######################################
async def getServerInfo(db_arr, x):

    if debug == True:
        print("%s\n#######################################\n#%s             Server Query            %s#\n#######################################%s" % (cSubTitle, cNormal, cSubTitle, cNormal))

    serverIP = db_arr[x][1]
    serverQPort = db_arr[x][3]

    if debug == True:
        print("%sServer IP:%s %s" % (cInfo, cNormal, serverIP))
        print("%sServer Query Port:%s %s" % (cInfo, cNormal, serverQPort))
    
    # Assign the IP and Query Port to address variable
    # IP needs to be a string, Query Port needs to be an int.
    address = (str(serverIP), int(serverQPort))

    if db_arr[x][4] == 'Minecraft':
        exceptionType = ConnectionRefusedError
    else:
        exceptionType = TimeoutError
        
    try: 
        if db_arr[x][4] == 'Minecraft':
            serverInfo = JavaServer("%s" %(serverIP), serverQPort)
            serverStatus = serverInfo.status()
            serverQuery = serverInfo.query()
        
            server_arr = ["Minecraft", serverQuery.map, serverStatus.players.online, serverStatus.players.max]
            if debug == True:
                print("%sServer Array:%s %s" % (cInfo, cNormal, server_arr))
        else: 
            serverInfo = a2s.info(address)
            if debug == True:
                print("%sServer Info:%s %s" % (cInfo, cNormal, serverInfo))

            server_arr = [serverInfo.server_name, serverInfo.map_name, serverInfo.player_count, serverInfo.max_players]
            if debug == True:
                print("%sServer Array:%s %s" % (cInfo, cNormal, server_arr))
    except exceptionType: 
        server_arr = 'NULL'
        if debug == True:
            print("%sServer Query Timed Out!%s" % (cError, cNormal))
            print("%sThe server is either offline or not accessible!%s" % (cError, cNormal))
    
    # Get the player information
    if showPlayerNamesInEmbed == True:
        if debug == True:
            print("\n%sshowPlayerNamesInEmbed is Enabled!%s" % (cSuccess, cNormal))

        try:
            if db_arr[x][4] == 'Minecraft':
                serverInfo = JavaServer("%s" %(serverIP), serverQPort)
                playerInfo = serverInfo.query()
            else: 
                playerInfo = a2s.players(address)

            if db_arr[x][4] == 'Minecraft':
                if serverStatus.players.online == 0:
                    players_arr = 'NULL'
                    if debug == True:
                        print("\n%sNo Players Online!%s" % (cError, cNormal))
                else:
                    # Prepare the players array
                    w = int(playerInfo.players.online)
                    if debug == True:
                        print("\n%sTotal Players Online: %s%s" % (cInfo, cNormal, w))

                    players_arr = [0 for a in range(w + 1)] 
                    y = 0
                    while y <= w: 
                        # This is a gross workaround to an issue I noticed with players
                        # the player count will show 3 players
                        # but will only show 2 player names
                        # seems like '\n'.join(players_arr) will cut off the first index every time
                        # so I am filling the first index with garbage that will be cut off anyways
                        # and filling the rest of the array with player names
                        z = y - 1
                        if y == 0:
                            players_arr[y] = 'aosidj'
                        else: 
                            players_arr[y] = playerInfo.players.names[z]
                        y += 1
                    if debug == True:
                        print("\n%sOnline Players: \n%s%s" % (cInfo, cNormal, players_arr))
            else:
                if playerInfo == []:
                    players_arr = 'NULL'
                    if debug == True:
                        print("\n%sNo Players Online!%s" % (cError, cNormal))
                else:
                    # Prepare the players array
                    w = int(len(playerInfo))
                    if debug == True:
                        print("\n%sTotal Players Online: %s%s" % (cInfo, cNormal, w))
                    players_arr = [0 for a in range(w + 1)] 
                    y = 0
                    while y <= w: 
                        # This is a gross workaround to an issue I noticed with players
                        # the player count will show 3 players
                        # but will only show 2 player names
                        # seems like '\n'.join(players_arr) will cut off the first index every time
                        # so I am filling the first index with garbage that will be cut off anyways
                        # and filling the rest of the array with player names
                        z = y - 1
                        if y == 0:
                            players_arr[y] = 'aosidj'
                        else: 
                            players_arr[y] = playerInfo[z].name
                        y += 1
                    if debug == True:
                        print("\n%sOnline Players: \n%s%s" % (cInfo, cNormal, players_arr))

        except TimeoutError: 
            players_arr = 'NULL'
                
            if debug == True:
                print("%sPlayer Query Timed Out!%s" % (cError, cNormal))
    else:
        players_arr = 'NULL'
                
        if debug == True:
            print("\n%sshowPlayerNamesInEmbed is disabled!%s" % (cError, cNormal))

    channel = db_arr[x][6]

    # call function sendEmbed 'None' is for the exception check, this can literally be anything.
    # except 'Message' as that will send a new message to the channel
    await sendEmbed(client.get_channel(channel), db_arr, server_arr, players_arr, x, 'None')
    
#######################################
#         Send Embed Message          #
#######################################
async def sendEmbed(channel, db_arr, server_arr, players_arr, x, exception):
    if debug == True:
        print("%s\n#######################################\n#%s         Send Embed Message          %s#\n#######################################%s" % (cSubTitle, cNormal, cSubTitle, cNormal))

    serverIP = db_arr[x][1]
    serverPort = db_arr[x][2]
    serverQPort = db_arr[x][3]
    serverGame = db_arr[x][4]
    serverTitle = db_arr[x][5]
    channel_ID = db_arr[x][6]
    message_ID = db_arr[x][7]

    if debug == True:
        print("%sServer IP:%s %s" %(cInfo, cNormal, serverIP))
        print("%sServer Port:%s %s" %(cInfo, cNormal, serverPort))
        print("%sServer Query Port:%s %s" %(cInfo, cNormal, serverQPort))
        print("%sServer Game:%s %s" %(cInfo, cNormal, serverGame))
        print("%sServer Title:%s %s" %(cInfo, cNormal, serverTitle))
        print("%sChannel ID:%s %s" %(cInfo, cNormal, channel_ID))
        print("%sMessage ID:%s %s" %(cInfo, cNormal, message_ID))


    if showTimestamp == True:
        timestamp = datetime.now(datetime.utcnow().astimezone().tzinfo)
        if debug == True:
            print("%sTimestamp:%s %s" %(cInfo, cNormal, timestamp))
    else:
        timestamp = None
        if debug == True:
            print("%sTimestamp is disabled!%s" %(cError, cNormal))
    if useServerNameAsTitle == True:
        title = server_arr[0]
        if debug == True:
            print("%sUsing server name as embed title!%s" %(cSuccess, cNormal))
    else:
        title = serverTitle
        if debug == True:
            print("%sUsing database name as embed title!%s" %(cSuccess, cNormal))
    if debug == True:
        print("%sEmbed Title:%s %s" %(cInfo, cNormal, title))

    # If exception is caught, when editing message (i.e. the message was deleted), assign 0 to message_ID, this will make the bot send new message
    if exception == 'Message':
        message_ID = 0
        if debug == True:
            print("%sResending Message!%s" %(cError, cNormal))
    # else, just get the messageID from the database
    else:
        message_ID = int(message_ID)

    # Get channel ID from database and assign it with get_channel
    channel_ID = client.get_channel(channel_ID)

    embedVar = discord.Embed(title=title, color=discord.Color.from_str(embedColor), timestamp=timestamp)
    # If getServerInfo() was able to query server (i.e. the server is online), this will not be NULL, will send server info
    if server_arr != 'NULL':
        if debug == True:
            print("%sServer Is Online! %s" %(cSuccess, cNormal))

        embedVar.set_thumbnail(url = thumbnailImage)
        if showDirectConnectInEmbed == True:
            embedVar.add_field(name="Direct Connect:", value="`%s:%s`" % (serverIP, serverPort), inline=True)
        if showGameInEmbed == True:
            embedVar.add_field(name="Game:", value="`%s`" %serverGame, inline=True)
        if showMapInEmbed == True:
            embedVar.add_field(name="Map:", value="`%s`" %server_arr[1], inline=True)
        if showCurrentPlayersInEmbed == True:
            embedVar.add_field(name="Current Players:", value="`%s/%s`" % (server_arr[2], server_arr[3]), inline=True)
        if showSteamConnectionInEmbed == True:
            embedVar.add_field(name="Steam Connection:", value="steam://connect/%s:%s" % (serverIP, serverPort), inline=True)
        if showPlayerNamesInEmbed == True:
            if debug == True:
                print("%sshowPlayerNamesInEmbed is enabled! %s" %(cSuccess, cNormal))
            if players_arr != 'NULL':
                #players = '\n'.join(players_arr) + ' '
                players = '\n'.join(players_arr)
                embedVar.add_field(name="Current Players Online:", value="```%s```" % (players), inline=False)
                if debug == True:
                    print("%sCurrent Online Players: \n%s%s" %(cInfo, cNormal, players))
            else:
                if debug == True:
                    print("%sNo Players Online! %s" %(cError, cNormal))
        embedVar.set_footer(text=footerNote, icon_url=footerImage)
    # If get ServerInfo() wasn't able to query server (i.e. the server is offline), 
    # server_arr will be NULL and will display "server offline" message instead
    # This wont use all of the configs as you will want to know when the server 
    # was last checked, color will be different, etc.
    else:
        if debug == True:
            print("%sServer Is Offline!%s" %(cError, cNormal))
        embedVar = discord.Embed(title=serverTitle, color=0xFF0000, timestamp=datetime.now(datetime.utcnow().astimezone().tzinfo), description="<:error:1047015196473962537> This server is either unable to be reached or is in an offline state.")
        embedVar.set_footer(text=footerNote, icon_url=footerImage)
    # if the message_ID = 0, then it is either, a new server or it threw an exception in the check in the else statment
    if message_ID == 0:
        message_ID = await channel_ID.send(embed=embedVar)
        if debug == True:
            print("%sSending New Message to %s!\nNew Message: %s%s" %(cInfo, channel_ID, message_ID, cNormal))
        await sendMessageInfo(message_ID, x)
    else:
        if debug == True:
            print("%sTrying to edit message!%s" %(cInfo, cNormal))
        # Try to edit the message, if it's there, edit the message.
        try:
            msg = await channel_ID.fetch_message(message_ID)
            await msg.edit(embed=embedVar)
            if debug == True:
                print("%sSuccess!%s" %(cSuccess, cNormal))
        except discord.errors.NotFound:
            if debug == True:
                print("%sException Raised!%s" %(cError, cNormal))
            # if the bot doesn't find the message (i.e. the message was deleted)
            # it will just send a new one and replace the id with the new one
            await sendEmbed(channel, db_arr, server_arr, players_arr, x, 'Message')

#############################################################################
# to_thread and wait func are only here to prevent 'heartbeat blocked for   #
# more than 10 seconds.' error, or else I would be using time.sleep by      #
# itself                                                                    #
#############################################################################
def to_thread(func: typing.Callable) -> typing.Coroutine:                   #
    @functools.wraps(func)                                                  #
    async def wrapper(*args, **kwargs):                                     #
        return await asyncio.to_thread(func, *args, **kwargs)               #
    return wrapper                                                          #
                                                                            #
@to_thread                                                                  #
def wait(a):                                                                #
    if a > 5:                                                              #
        print("%sWaiting %s seconds...%s" %(cInfo, a, cNormal))             #
    time.sleep(a)                                                           #
#############################################################################

@client.event
async def on_ready():
    if debug == True:
        print("%sBot is ready!%s" %(cSuccess, cNormal))
        await getDBInfo(9, a = 0)
    a = 1
    while True:
        await update_config()
        x = 0
    
        # This is the workaround I found to get the number of servers in the database, this will just call getDBInfo with a new param
        # which will stop it from calling getServerInfo(), and just return the servers array, which we can get the length
        # then we can just run the rest of the script like usual
        # and another added benefit is that since this is in the while loop every x seconds it will check the server for updates and
        # update the servers count so if we add a server, next time its ran it will get the most up-to-date server count instead of 
        # having to restart the script when a server is added/removed
        numOfServers = len(await getDBInfo(x, a = 1))
    
        while x <= numOfServers - 1:
            if debug == True:
                print("%sServer Index: %s%s" %(cSuccess, cNormal, x))
            # wait(5) is here to prevent Discord from rate limiting the bot, which will force you to wait about 4-5 seconds anyway
            await wait(5)
            await getDBInfo(x, a = 0)
            x += 1

        if a == 1:
            print("%sServer Status has run %s time since last restart!%s" %(cInfo, a, cNormal))
        else:
            print("%sServer Status has run %s times since last restart!%s" %(cInfo, a, cNormal))
        # Prevents user from using ctrl+c to exit script, you need to wait till after the wait function is done
        await wait(int(config['GENERAL']['refreshTime']))
        a += 1

client.run(config['TOKEN']['bottoken'])