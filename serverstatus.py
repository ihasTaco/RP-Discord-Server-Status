import configparser
import mariadb
import os
from datetime import datetime, timedelta
import time
import discord
from discord.utils import get
import a2s
from mcstatus import JavaServer
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import random
import string

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def colors(x):
    if x == 'Debug':
        return '\033[1;32m'
    if x == 'SubTitle':
        return '\033[0;36m'
    if x == 'Error':
        return '\033[1;91m'
    if x == 'Success':
        return '\033[1;92m'
    if x == 'Normal':
        return '\033[0;00m'
    if x == 'Info':
        return '\033[0;33m'

# Token Settings
token = None
# Database Settings
dbHost = None
dbUser = None
dbPassword = None
dbDatabase = None
dbTable = None
db = None

# Debug Settings
debug = None

# General Embed Settings
refreshTime = None
thumbnailImage = None
embedColor = None
useServerNameAsTitle = None
showDirectConnectInEmbed = None
showServerLocation = None
showGameInEmbed = None
showMapInEmbed = None
showCurrentPlayersInEmbed = None
showSteamConnectionInEmbed = None
showPlayerNamesInEmbed = None
showTimestamp = None
footerNote = None
footerImage = None

# Graph Settings
graphEnabled = None
graphTitle = None
graphLabel = None
graphXLabel = None
graphYLabel = None
discordImageChannel = None
graphColor = None
showServerPeak = None
deleteImagesInDiscord = None
graphBorderTopOpacity = None
graphBorderBottomOpacity = None
graphBorderLeftOpacity = None
graphBorderRightOpacity = None
graphXAxisLabelOpacity = None
graphYAxisLabelOpacity = None
graphTitleOpacity = None
graphXLabelOpacity = None
graphYLabelOpacity = None
graphFillOpacity = None

timestamp_arr = None
players_arr = None
    
def connectDB():
    global dbHost
    global dbUser
    global dbPassword
    global dbDatabase
    # db needs to be a global variable as it needs to be accessed in multiple functions
    try:
        global db
        db = mariadb.connect(
            host=dbHost,
            user=dbUser,
            password=dbPassword,
            database=dbDatabase
        )
        print("\n%sSuccessfully connected to database!%s" % (colors('Success'), colors('Normal')))
        
    except mariadb.OperationalError:
        print("\n%sFailed to connect to database!%s" % (colors('Error'), colors('Normal')))
        print("%sMake sure you typed in the correct information!%s" % (colors('Error'), colors('Normal')))

def updateConfig():
    exec(open("config.py").read())
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')

    global debug
    debug = bool(config['GENERAL']['debugmode'] == 'True')

    if debug == True:
        print("%s\n#######################################\n#%s           Debug Mode: On            %s#\n#######################################\n%s" %(colors('Debug'), colors('Normal'), colors('Debug'), colors('Normal')))

    # Get information from config
    global token
    global dbHost
    global dbUser
    global dbPassword
    global dbDatabase
    global dbTable
    global db
    global embedColor
    global showPlayerNamesInEmbed
    global showDirectConnectInEmbed
    global showServerLocation
    global showGameInEmbed
    global showMapInEmbed
    global showCurrentPlayersInEmbed
    global showSteamConnectionInEmbed
    global useServerNameAsTitle
    global showTimestamp
    global refreshTime
    global graphEnabled
    global graphLabel
    global graphTitle
    global graphXLabel
    global graphYLabel
    global discordImageChannel
    global graphColor
    global showServerPeak
    global deleteImagesInDiscord
    global graphBorderTopOpacity
    global graphBorderBottomOpacity
    global graphBorderLeftOpacity
    global graphBorderRightOpacity
    global graphXAxisLabelOpacity
    global graphYAxisLabelOpacity
    global graphTitleOpacity
    global graphXLabelOpacity
    global graphYLabelOpacity
    global graphFillOpacity

    token = config['TOKEN']['botToken']
    dbHost = config['DATABASE']['host']
    dbUser = config['DATABASE']['user']
    dbPassword = config['DATABASE']['password']
    dbDatabase = config['DATABASE']['database']
    dbTable = config['DATABASE']['table']
    embedColor = config['GENERAL']['embedColor']
    showPlayerNamesInEmbed = bool(config['GENERAL']['showplayernamesinembed'] == 'True')
    showDirectConnectInEmbed = bool(config['GENERAL']['showDirectConnectInEmbed'] == 'True')
    showServerLocation = bool(config['GENERAL']['showServerLocation'] == 'True')
    showGameInEmbed = bool(config['GENERAL']['showGameInEmbed'] == 'True')
    showMapInEmbed = bool(config['GENERAL']['showMapInEmbed'] == 'True')
    showCurrentPlayersInEmbed = bool(config['GENERAL']['showCurrentPlayersInEmbed'] == 'True')
    showSteamConnectionInEmbed = bool(config['GENERAL']['showSteamConnectionInEmbed'] == 'True')
    useServerNameAsTitle = bool(config['GENERAL']['useservernameastitle'] == 'True')
    showTimestamp = bool(config['GENERAL']['showtimestamp'] == 'True')
    refreshTime = int(config['GENERAL']['refreshtime'])

    graphEnabled = bool(config['GRAPH']['graphEnabled'] == 'True')
    graphLabel = str(config['GRAPH']['graphLabel'])
    graphTitle = str(config['GRAPH']['graphTitle'])
    graphXLabel = str(config['GRAPH']['graphXLabel'])
    graphYLabel = str(config['GRAPH']['graphYLabel'])
    discordImageChannel = int(config['GRAPH']['discordImageChannel'])
    graphColor = str(config['GRAPH']['graphColor'])
    showServerPeak = bool(config['GRAPH']['showServerPeak'] == 'True')
    deleteImagesInDiscord = bool(config['GRAPH']['deleteImagesInDiscord'] == 'True')
    graphBorderTopOpacity = float(config['GRAPH']['graphBorderTopOpacity'])
    graphBorderBottomOpacity = float(config['GRAPH']['graphBorderBottomOpacity'])
    graphBorderLeftOpacity = float(config['GRAPH']['graphBorderLeftOpacity'])
    graphBorderRightOpacity = float(config['GRAPH']['graphBorderRightOpacity'])
    graphXAxisLabelOpacity = float(config['GRAPH']['graphXAxisLabelOpacity'])
    graphYAxisLabelOpacity = float(config['GRAPH']['graphYAxisLabelOpacity'])
    graphTitleOpacity = float(config['GRAPH']['graphTitleOpacity'])
    graphXLabelOpacity = float(config['GRAPH']['graphXLabelOpacity'])
    graphYLabelOpacity = float(config['GRAPH']['graphYLabelOpacity'])
    graphFillOpacity = float(config['GRAPH']['graphFillOpacity'])

    global thumbnailImage
    if config['GENERAL']['thumbnailimage'] == '':
        thumbnailImage = None
    else:
        thumbnailImage = config['GENERAL']['thumbnailimage']
    global footerNote
    if config['GENERAL']['footernote'] == '':
        footerNote = None
    else:
        footerNote = config['GENERAL']['footernote']
    
    global footerImage
    if config['GENERAL']['footerimage'] == '':
        footerImage = None
    else:
        footerImage = config['GENERAL']['footerimage']

    if debug == True:
        print("\n%s--- Database Config Variable Initialization ---%s" % (colors('Info'), colors('Normal')))
        print("%sDatabase Host:%s %s" % (colors('Info'), colors('Normal'), dbHost))
        print("%sDatabase User:%s %s" % (colors('Info'), colors('Normal'), dbUser))
        print("%sDatabase Password:%s %s" % (colors('Info'), colors('Normal'), dbPassword))
        print("%sDatabase Database:%s %s" % (colors('Info'), colors('Normal'), dbDatabase))
        print("%sDatabase Table:%s %s" % (colors('Info'), colors('Normal'), dbTable))
        print('')
        print("\n%s--- General Config Variable Initialization ---%s" % (colors('Info'), colors('Normal')))
        print("%sembedColor:%s %s" % (colors('Info'), colors('Normal'), embedColor))
        print("%sthumbnailImage:%s %s" % (colors('Info'), colors('Normal'), thumbnailImage))
        print("%sfooterNote:%s %s" % (colors('Info'), colors('Normal'), footerNote))
        print("%sfooterImage:%s %s" % (colors('Info'), colors('Normal'), footerImage))
        print("%sshowPlayerNamesInEmbed:%s %s" % (colors('Info'), colors('Normal'), showPlayerNamesInEmbed))
        print("%sshowDirectConnectInEmbed:%s %s" % (colors('Info'), colors('Normal'), showDirectConnectInEmbed))
        print("%sshowServerLocation:%s %s" % (colors('Info'), colors('Normal'), showServerLocation))
        print("%sshowGameInEmbed:%s %s" % (colors('Info'), colors('Normal'), showGameInEmbed))
        print("%sshowMapInEmbed:%s %s" % (colors('Info'), colors('Normal'), showMapInEmbed))
        print("%sshowCurrentPlayersInEmbed:%s %s" % (colors('Info'), colors('Normal'), showCurrentPlayersInEmbed))
        print("%sshowSteamConnectionInEmbed:%s %s" % (colors('Info'), colors('Normal'), showSteamConnectionInEmbed))
        print("%suseServerNameAsTitle:%s %s" % (colors('Info'), colors('Normal'), useServerNameAsTitle))
        print("%sshowTimestamp:%s %s" % (colors('Info'), colors('Normal'), showTimestamp))
        print('')
        print("\n%s--- Graph Config Variable Initialization ---%s" % (colors('Info'), colors('Normal')))
        print("%sgraphEnabled:%s %s" % (colors('Info'), colors('Normal'), graphEnabled))
        print("%sgraphTitle:%s %s" % (colors('Info'), colors('Normal'), graphTitle))
        print("%sgraphLabel:%s %s" % (colors('Info'), colors('Normal'), graphLabel))
        print("%sdiscordImageChannel:%s %s" % (colors('Info'), colors('Normal'), discordImageChannel))
        print("%sgraphColor:%s %s" % (colors('Info'), colors('Normal'), graphColor))
        print("%sshowServerPeak:%s %s" % (colors('Info'), colors('Normal'), showServerPeak))
        print("%sdeleteImagesInDiscord:%s %s" % (colors('Info'), colors('Normal'), deleteImagesInDiscord))
        print("%sgraphBorderTopOpacity:%s %s" % (colors('Info'), colors('Normal'), graphBorderTopOpacity))
        print("%sgraphBorderBottomOpacity:%s %s" % (colors('Info'), colors('Normal'), graphBorderBottomOpacity))
        print("%sgraphBorderLeftOpacity:%s %s" % (colors('Info'), colors('Normal'), graphBorderLeftOpacity))
        print("%sgraphBorderRightOpacity:%s %s" % (colors('Info'), colors('Normal'), graphBorderRightOpacity))
        print("%sgraphXAxisLabelOpacity:%s %s" % (colors('Info'), colors('Normal'), graphXAxisLabelOpacity))
        print("%sgraphYAxisLabelOpacity:%s %s" % (colors('Info'), colors('Normal'), graphYAxisLabelOpacity))
        print("%sgraphTitleOpacity:%s %s" % (colors('Info'), colors('Normal'), graphTitleOpacity))
        print("%sgraphXLabelOpacity:%s %s" % (colors('Info'), colors('Normal'), graphXLabelOpacity))
        print("%sgraphYLabelOpacity:%s %s" % (colors('Info'), colors('Normal'), graphYLabelOpacity))
        print("%sgraphFillOpacity:%s %s" % (colors('Info'), colors('Normal'), graphFillOpacity))

class database:
    def initial():
        global debug
        global db
        global dbTable

        if debug == True:
            print("%s\n#######################################\n#%s      Initial SQL Server Query       %s#\n#######################################%s" % (colors('SubTitle'), colors('Normal'), colors('SubTitle'), colors('Normal')))
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM %s" %dbTable)
        results = cursor.fetchall()

        if debug == True:
            print("%sSELECT * FROM %s%s" %(colors('Info'), dbTable, colors('Normal')))
            if results == []:
                print("%sNothing is in the database!\nCheck to make sure your database is set up correctly!%s" % (colors('Error'), colors('Normal')))
                os._exit(1)
            else:
                print("%sSuccessfully found %s rows! %s" % (colors('Success'), len(results), colors('Normal')))

        return results

    def query(db_index):
        global debug
        global db
        global dbTable

        if debug == True:
            print("%s\n#######################################\n#%s          SQL Server Query           %s#\n#######################################%s" % (colors('SubTitle'), colors('Normal'), colors('SubTitle'), colors('Normal')))
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM %s WHERE ID=%s" %(dbTable, db_index))
        results = cursor.fetchall()

        # Fill servers array with 0's to appropriate sizes
        w, h = 9, 1
        servers = [[0 for a in range(w)] for b in range(h)] 
        # start assigning results to servers array
        for y in results:
            z = 0
            while z <= len(y) - 1: 
                servers[0][z] = y[ z ]
                z += 1

        if debug == True:
            print('%sResults: %s\n%s' %(colors('Info'), colors('Normal'), servers))

        return servers

    class submit:
        def channel(message, x):
            global debug
            global db
            global dbTable
            if debug == True:
                print("%s\n#######################################\n#%s    Send Message Info to Database    %s#\n#######################################%s" % (colors('SubTitle'), colors('Normal'), colors('SubTitle'), colors('Normal')))
            message = str(message).split()
            message = str(message[1]).split('id=')

            if debug == True:
                print("%sMessage ID:%s %s" % (colors('Info'), colors('Normal'), message[1]))
            cursor = db.cursor()
            cursor.execute('UPDATE server_info SET messageID = \"%s\" WHERE ID = \"%s\"' % (str(message[1]), x))
            db.commit()
            if debug == True:
                print("%sMessage ID Sent to Database Successfully!%s" % (colors('Success'), colors('Normal')))

        def server(ip, port, qport, game, name, channel_id, location):
            global debug
            global db
            global dbTable
            if debug == True:
                print("%s\n#######################################\n#%s    Send Server Info to Database    %s#\n#######################################%s" % (colors('SubTitle'), colors('Normal'), colors('SubTitle'), colors('Normal')))
            if debug == True:
                print("%sIP:%s %s" % (colors('Info'), colors('Normal'), ip))
                print("%sPort:%s %s" % (colors('Info'), colors('Normal'), port))
                print("%sQuery Port:%s %s" % (colors('Info'), colors('Normal'), qport))
                print("%sGame:%s %s" % (colors('Info'), colors('Normal'), game))
                print("%sServer Name:%s %s" % (colors('Info'), colors('Normal'), name))
                print("%sChannel ID:%s %s" % (colors('Info'), colors('Normal'), channel_id))
                print("%sServer Location:%s %s" % (colors('Info'), colors('Normal'), location))
            cursor = db.cursor()
            cursor.execute('INSERT INTO server_info (IP, Port, Query_Port, Game, Server_Name, ChannelID, server_location) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")' % (ip, port, qport, game, name, channel_id, location))
            db.commit()
            if debug == True:
                print("%sServer Info Sent to Database Successfully!%s" % (colors('Success'), colors('Normal')))

    def delete(db_index: int):
        global debug
        global db
        global dbTable

        if debug:
            print("%s\n#######################################\n#%s          Delete Server              %s#\n#######################################%s" % (colors('SubTitle'), colors('Normal'), colors('SubTitle'), colors('Normal')))

        # Create a cursor to execute the SQL query
        cursor = db.cursor()
        # Execute the DELETE query using the `db_index`
        cursor.execute("DELETE FROM %s WHERE ID=%s" % (dbTable, db_index))
        # Save the changes to the database
        db.commit()

        if debug:
            print("%sSuccessfully deleted server with index %s from the database%s" % (colors('Success'), db_index, colors('Normal')))
    def reset_auto_increment():
        global debug
        global db
        global dbTable
        print('reset')
        cursor = db.cursor()

        sql = f"ALTER TABLE {dbTable} AUTO_INCREMENT = 0"
        cursor.execute(sql)

        db.commit()

class server:
    def minecraft(db_arr, x):
        if debug == True:
            print("%s\n#######################################\n#%s             Server Query            %s#\n#######################################%s" % (colors('SubTitle'), colors('Normal'), colors('SubTitle'), colors('Normal')))

        serverIP = db_arr[0][1]
        serverQPort = db_arr[0][3]

        if debug == True:
            print("%sServer IP:%s %s" % (colors('Info'), colors('Normal'), serverIP))
            print("%sServer Query Port:%s %s" % (colors('Info'), colors('Normal'), serverQPort))

        address = (str(serverIP), int(serverQPort))

        try:
            serverInfo = JavaServer("%s" %(serverIP), serverQPort)
            serverStatus = serverInfo.status()
            serverQuery = serverInfo.query()

            server_arr = ["Minecraft", serverQuery.map, serverStatus.players.online, serverStatus.players.max]
            if debug == True:
                print("%sServer Array:%s %s" % (colors('Info'), colors('Normal'), server_arr))

        except ConnectionRefusedError: 
            server_arr = 'NULL'
            print("%sGame: %s%s" %(colors('Error'), server_arr[0], colors('Normal')))
            print("%sServer Query Timed Out!%s" % (colors('Error'), colors('Normal')))
            print("%sThe server is either offline or not accessible!%s" % (colors('Error'), colors('Normal')))
        
        # Get the player information
        if showPlayerNamesInEmbed == True:
            if debug == True:
                print("\n%sshowPlayerNamesInEmbed is Enabled!%s" % (colors('Success'), colors('Normal')))

            try:
                serverInfo = JavaServer("%s" %(serverIP), serverQPort)
                playerInfo = serverInfo.query()

                if serverStatus.players.online == 0:
                    players_arr = 'NULL'
                    if debug == True:
                        print("\n%sNo Players Online!%s" % (colors('Error'), colors('Normal')))
                else:
                    # Prepare the players array
                    w = int(playerInfo.players.online)

                    if debug == True:
                        print("\n%sTotal Players Online: %s%s" % (colors('Info'), colors('Normal'), w))

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
                            players_arr[y] = ''
                        else: 
                            players_arr[y] = playerInfo.players.names[z]
                        y += 1
                    if debug == True:
                        print("\n%sOnline Players: \n%s%s" % (colors('Info'), colors('Normal'), players_arr))

            except TimeoutError: 
                players_arr = 'NULL'

                print("%sPlayer Query Timed Out!%s" % (colors('Error'), colors('Normal')))
        else:
            players_arr = 'NULL'

            if debug == True:
                print("\n%sshowPlayerNamesInEmbed is disabled!%s" % (colors('Error'), colors('Normal')))

        return server_arr, players_arr

    def source(db_arr, x):

        if debug == True:
            print("%s\n#######################################\n#%s             Server Query            %s#\n#######################################%s" % (colors('SubTitle'), colors('Normal'), colors('SubTitle'), colors('Normal')))

        serverIP = db_arr[0][1]
        serverQPort = db_arr[0][3]

        if debug == True:
            print("%sServer IP:%s %s" % (colors('Info'), colors('Normal'), serverIP))
            print("%sServer Query Port:%s %s" % (colors('Info'), colors('Normal'), serverQPort))

        address = (str(serverIP), int(serverQPort))

        try: 
            serverInfo = a2s.info(address)
            server_arr = [serverInfo.server_name, serverInfo.map_name, serverInfo.player_count, serverInfo.max_players]

            if debug == True:
                print("%sServer Array:%s %s" % (colors('Info'), colors('Normal'), server_arr))

        except TimeoutError: 
            server_arr = 'NULL'
            print("%sGame: %s%s" %(colors('Error'), colors('Normal'), db_arr[0][4]))
            print("%sServer Query Timed Out!%s" % (colors('Error'), colors('Normal')))
            print("%sThe server is either offline or not accessible!%s" % (colors('Error'), colors('Normal')))

        # Get the player information
        if showPlayerNamesInEmbed == True:
            if debug == True:
                print("\n%sshowPlayerNamesInEmbed is Enabled!%s" % (colors('Success'), colors('Normal')))

            try:
                playerInfo = a2s.players(address)

                if playerInfo == []:
                    players_arr = 'NULL'
                    if debug == True:
                        print("\n%sNo Players Online!%s" % (colors('Error'), colors('Normal')))
                else:
                    # Prepare the players array
                    w = int(len(playerInfo))
                    if debug == True:
                        print("\n%sTotal Players Online: %s%s" % (colors('Info'), colors('Normal'), w))
                    players_arr = [0 for a in range(w + 1)] 
                    y = 0
                    while y <= w: 
                        z = y - 1
                        if y == 0:
                            players_arr[y] = 'aosidj'
                        else: 
                            players_arr[y] = playerInfo[z].name
                        y += 1
                    if debug == True:
                        print("\n%sOnline Players: \n%s%s" % (colors('Info'), colors('Normal'), players_arr))

            except TimeoutError: 
                players_arr = 'NULL'

                print("%sPlayer Query Timed Out!%s" % (colors('Error'), colors('Normal')))
        else:
            players_arr = 'NULL'

            if debug == True:
                print("\n%sshowPlayerNamesInEmbed is disabled!%s" % (colors('Error'), colors('Normal')))

        return server_arr, players_arr

class graph:
    def initial_plot():
        global players_arr
        global timestamp_arr

        w, h = 288, len(database.initial())
        timestamp_arr = [[datetime.today() - timedelta(days = 1) for a in range(w)] for b in range(h)]
        players_arr = [[0 for a in range(w)] for b in range(h)]

    def line_plot(x, players, h):
        global graphTitle
        global graphLabel
        global graphXLabel
        global graphYLabel
        global graphBorderTopOpacity
        global graphBorderBottomOpacity
        global graphBorderLeftOpacity
        global graphBorderRightOpacity
        global graphXAxisLabelOpacity
        global graphYAxisLabelOpacity
        global graphTitleOpacity
        global graphXLabelOpacity
        global graphYLabelOpacity
        global graphFillOpacity

        fig = plt.figure()

        z = md.num2date(x, tz=None)

        # converts HEX into RGBA values
        RGB = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        b = [x / 255.0 for x in RGB]

        plt.plot(z, players, label = graphLabel, color=(b[0], b[1], b[2], 1))
        plt.legend() 
        plt.xlabel(graphXLabel)
        plt.ylabel(graphYLabel)
        plt.title(graphTitle)
        plt.margins(0)
        ax=plt.gca()
        ax.set_ylim([0, max(players) + 5])

        loc = ticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
        ax.yaxis.set_major_locator(loc)

        xfmt = md.DateFormatter('%I %p')
        ax.xaxis.set_major_formatter(xfmt)

        # Setting Colors 
        ax.spines['bottom'].set_color((b[0], b[1], b[2], graphBorderBottomOpacity))
        ax.spines['top'].set_color((b[0], b[1], b[2], graphBorderTopOpacity))
        ax.spines['right'].set_color((b[0], b[1], b[2], graphBorderRightOpacity))
        ax.spines['left'].set_color((b[0], b[1], b[2], graphBorderLeftOpacity))
        ax.tick_params(axis='x', colors=(b[0], b[1], b[2], graphXAxisLabelOpacity))
        ax.tick_params(axis='y', colors=(b[0], b[1], b[2], graphYAxisLabelOpacity))
        ax.yaxis.label.set_color((b[0], b[1], b[2], graphYLabelOpacity))
        ax.xaxis.label.set_color((b[0], b[1], b[2], graphXLabelOpacity))
        ax.title.set_color((b[0], b[1], b[2], graphTitleOpacity))
        plt.fill_between(x, players, 0, color=(b[0], b[1], b[2], graphFillOpacity))

        ax.tick_params(axis='x', labelrotation = 45)

        url = "images/"
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        filename = result_str + '.png'
        plt.savefig('images/' + filename, transparent=True)

        plt.close()

        #plt.show()
        max_value = max(players)
        peakIndex = players.index(max_value)

        return url + filename, max_value, z[peakIndex].strftime("%I %p")

    def plot(server_index, players):
        global graphColor
        global embedColor
        global players_arr
        global timestamp_arr

        if graphColor != '':
            color = graphColor
        else:
            color = embedColor
        
        timestamp = np.datetime64(datetime.today())
        timestamp_arr[server_index].append(timestamp)
        players_arr[server_index].append(players)
        return graph.line_plot(md.date2num(timestamp_arr[server_index]), players_arr[server_index], str(color))