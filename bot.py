numOfServers = 9 # Put the actual number of servers in the DB **not the 0-Based number** 

import discord
from discord.utils import get
import mariadb
from datetime import datetime
import time
# For server query
import a2s
# For Bot Config
import configparser
# To stop blocking  
import functools
import typing
import asyncio

exec(open("config.py").read())

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Get Config
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

debug = config['GENERAL']['debugmode']
servers = []

db = mariadb.connect(
    host=config['DATABASE']['host'],
    user=config['DATABASE']['user'],
    password=config['DATABASE']['password'],
    database=config['DATABASE']['table']
)

async def getDBInfo(x):
    #######################################
    #          SQL Server Query           #
    #######################################

    cursor = db.cursor()
    cursor.execute("SELECT * FROM %s" %config['DATABASE']['database'])
    results = cursor.fetchall()

    if debug == True: 
        print('len(results): %s' %len(results))

    # Fill servers array with 0's to appropriate sizes
    w, h = 7, len(results)
    servers = [[0 for a in range(w)] for b in range(h)] 

    for y in results:
        z = 0
        while z <= 6: 
            servers[y[0]][z] = y[ z ]
            z += 1

    if debug == True: 
        print('Servers: \n %s' %servers)

    await getServerInfo(servers, x)

async def sendMessageInfo(message, x):
    #######################################
    #    Send Message Info to Database    #
    #######################################
    message = str(message).split()
    message = str(message[1]).split('id=')
    cursor = db.cursor()
    cursor.execute('UPDATE server_info SET messageInfo = \"%s\" WHERE ID = \"%s\"' % (str(message[1]), x))
    db.commit()
    

async def getServerInfo(db_arr, x):
    #######################################
    #             Server Query            #
    #######################################

    if debug == True: 
        print('IP: %s' %db_arr[x][1])
        print('Query Port: %s' %db_arr[x][3])

    address = ("%s" %db_arr[x][1], int(db_arr[x][3]))

    if debug == True: 
        print(a2s.info(address))

    try: 
        serverInfo = a2s.info(address)
        server_arr = [serverInfo.server_name, serverInfo.map_name, serverInfo.player_count, serverInfo.max_players]
    except TimeoutError: 
        server_arr = 'NULL'

    channel = db_arr[x][5]

    if debug == True: 
        print(channel)

    await sendEmbed(client.get_channel(channel), db_arr, server_arr, x, 'None')

async def sendEmbed(channel, db_arr, server_arr, x, exception):
    #######################################
    #         Send Embed Message          #
    #######################################
    if exception == 'Message':
        message_ID = 0
    else:
        message_ID = int(db_arr[x][6])
    
    channel_ID = client.get_channel(db_arr[x][5])
    
    if message_ID == 0:
        if server_arr != 'NULL':
            embedVar = discord.Embed(title="%s" %server_arr[0], color=0x00ff00, timestamp=datetime.now(datetime.utcnow().astimezone().tzinfo))
            embedVar.set_thumbnail(url = 'https://royalproductions.xyz/images/logo/RP_Logo_Outline.png')
            embedVar.add_field(name="Direct Connect:", value="`%s:%s`" % (db_arr[x][1], db_arr[x][2]), inline=True)
            embedVar.add_field(name="Game:", value="`%s`" %db_arr[x][4], inline=True)
            embedVar.add_field(name="Map:", value="`%s`" %server_arr[1], inline=True)
            embedVar.add_field(name="Server Players:", value="`%s/%s`" % (server_arr[2], server_arr[3]), inline=True)
            embedVar.add_field(name="Steam Connection:", value="steam://connect/%s:%s`" % (db_arr[x][1], db_arr[x][2]), inline=True)

            message_ID = await channel.send(embed=embedVar)
            await sendMessageInfo(message_ID, x)
        else:
            embedVar = discord.Embed(title="%s" %db_arr[x][4], color=0xFF0000, timestamp=datetime.now(datetime.utcnow().astimezone().tzinfo), description="<:error:1047015196473962537> This server is either unable to be reached or is in an offline state.")
            message_ID = await channel.send(embed=embedVar)
            await sendMessageInfo(message_ID, x)
    else: 
        try:
            if server_arr != 'NULL':
                embedVar = discord.Embed(title="%s" %server_arr[0], color=0x00ff00, timestamp=datetime.now(datetime.utcnow().astimezone().tzinfo))
                embedVar.set_thumbnail(url = 'https://royalproductions.xyz/images/logo/RP_Logo_Outline.png')
                embedVar.add_field(name="Direct Connect:", value="`%s:%s`" % (db_arr[x][1], db_arr[x][2]), inline=True)
                embedVar.add_field(name="Game:", value="`%s`" %db_arr[x][4], inline=True)
                embedVar.add_field(name="Map:", value="`%s`" %server_arr[1], inline=True)
                embedVar.add_field(name="Server Players:", value="`%s/%s`" % (server_arr[2], server_arr[3]), inline=True)
                embedVar.add_field(name="Steam Connection:", value="steam://connect/%s:%s`" % (db_arr[x][1], db_arr[x][2]), inline=True)

                if debug == True:
                    print("Working on server: %s" %x)

                msg = await channel_ID.fetch_message(message_ID)
                await msg.edit(embed=embedVar)
            else:
                embedVar = discord.Embed(title="%s" %db_arr[x][4], color=0xFF0000, timestamp=datetime.now(datetime.utcnow().astimezone().tzinfo), description="<:error:1047015196473962537> This server is either unable to be reached or is in an offline state.")
                
                if debug == True:
                    print("Working on server: %s" %x)

                msg = await channel_ID.fetch_message(message_ID)
                await msg.edit(embed=embedVar)
        except discord.errors.NotFound:
            # if the bot doesn't find the message (i.e. the message was deleted)
            # it will just send a new one and replace the id with the new one
            await sendEmbed(channel, db_arr, server_arr, x, 'Message')

# to_thread and wait func are only here to prevent 'heartbeat blocked for more than 10 seconds.' error,
# or else I would be using time.sleep by itself
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

@to_thread
def wait(a):
    time.sleep(a)

@client.event
async def on_ready():
    #await getDBInfo(x)
    while True:
        x = 0
        # Need to figure out how to get how many servers are in the database...
        # Might have to edit the getServerInfo func a bit to achieve this
        while x <= numOfServers - 1:
            await wait(5)
            await getDBInfo(x)
            x += 1

        # Prevents user from using ctrl+c to exit script, you need to wait till after the wait function is done
        await wait(60)

client.run(config['TOKEN']['bottoken'])



