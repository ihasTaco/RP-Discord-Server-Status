import discord
from discord.utils import get
import mariadb
# For server query
import a2s

# Get Bot Token
import botToken

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

debug = False
servers = []

async def getDBInfo(x):
    #######################################
    #          SQL Server Query           #
    #######################################
    mydb = mariadb.connect(
        host="localhost",
        user="root",
        password="",
        database="servers"
    )

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM server_info")
    results = cursor.fetchall()

    if debug == True: 
        print('len(results) - 1: %s' %len(results))

    # Fill servers array with 0's to appropriate sizes
    w, h = 6, len(results)
    servers = [[0 for a in range(w)] for b in range(h)] 

    for y in results:
        z = 0
        while z <= 5: 
            servers[y[0]][z] = y[ z ]
            z += 1

    if debug == True: 
        print('Servers: \n %s' %servers)

    await getServerInfo(servers, x)

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
        
    serverInfo = a2s.info(address)
    server_arr = [serverInfo.server_name, serverInfo.map_name, serverInfo.player_count, serverInfo.max_players]

    channel = db_arr[x][5]

    if debug == True: 
        print(channel)

    await sendEmbed(client.get_channel(channel), db_arr, server_arr, x)

async def sendEmbed(channel, db_arr, server_arr, x):
    #######################################
    #         Send Embed Message          #
    #######################################

    embedVar = discord.Embed(title="%s" %server_arr[0], color=0x00ff00)
    embedVar.add_field(name="Direct Connect:", value="`%s:%s`" % (db_arr[x][1], db_arr[x][2]), inline=True)
    embedVar.add_field(name="Game:", value="`%s`" %db_arr[x][4], inline=True)
    embedVar.add_field(name="Map:", value="`%s`" %server_arr[1], inline=True)
    embedVar.add_field(name="Server Players:", value="`%s/%s`" % (server_arr[2], server_arr[3]), inline=True)
    embedVar.add_field(name="Steam Connection:", value="steam://connect/%s:%s`" % (db_arr[x][1], db_arr[x][2]), inline=True)
    await channel.send(embed=embedVar)

@client.event
async def on_ready():
    x = 0
    while x <= 8:
        await getDBInfo(x)
        x += 1

client.run(botToken.getToken())