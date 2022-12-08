import discord
from discord.utils import get
import time 
import functools
import typing
import asyncio
import serverstatus
import os
os.system("")

cDebug = serverstatus.colors('Debug')
cSubTitle = serverstatus.colors('SubTitle')
cError = serverstatus.colors('Error')
cSuccess = serverstatus.colors('Success')
cNormal = serverstatus.colors('Normal')
cInfo = serverstatus.colors('Info')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

serverstatus.updateConfig()
serverstatus.connectDB()
serverstatus.graph.initial_plot()
servers = []


async def send(x, exception):
    db_arr = serverstatus.database.query(x)
    if db_arr[0][4] == 'Minecraft':
        server_arr, players_arr = serverstatus.server.minecraft(db_arr, x)
    else:
        server_arr, players_arr = serverstatus.server.source(db_arr, x)

    if serverstatus.debug == True:
        print("%s\n#######################################\n#%s         Send Embed Message          %s#\n#######################################%s" % (serverstatus.colors('SubTitle'), serverstatus.colors('Normal'), serverstatus.colors('SubTitle'), serverstatus.colors('Normal')))
    
    serverIP = db_arr[0][1]
    serverPort = db_arr[0][2]
    serverQPort = db_arr[0][3]
    serverGame = db_arr[0][4]
    serverTitle = db_arr[0][5]
    channel_ID = client.get_channel(db_arr[0][6])
    message_ID = db_arr[0][7]

    if serverstatus.debug == True:
        print("%sServer IP:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), serverIP))
        print("%sServer Port:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), serverPort))
        print("%sServer Query Port:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), serverQPort))
        print("%sServer Game:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), serverGame))
        print("%sServer Title:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), serverTitle))
        print("%sChannel ID:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), channel_ID))
        print("%sMessage ID:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), message_ID))
    if serverstatus.showTimestamp == True:
        timestamp = serverstatus.datetime.now(serverstatus.datetime.utcnow().astimezone().tzinfo)
        if serverstatus.debug == True:
            print("%sTimestamp:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), timestamp))
    else:
        timestamp = None
        if serverstatus.debug == True:
            print("%sTimestamp is disabled!%s" %(serverstatus.colors('Error'), serverstatus.colors('Normal')))
    if serverstatus.useServerNameAsTitle == True:
        title = server_arr[0]
        if serverstatus.debug == True:
            print("%sUsing server name as embed title!%s" %(serverstatus.colors('Success'), serverstatus.colors('Normal')))
    else:
        title = serverTitle
        if serverstatus.debug == True:
            print("%sUsing database name as embed title!%s" %(serverstatus.colors('Success'), serverstatus.colors('Normal')))
    if serverstatus.debug == True:
        print("%sEmbed Title:%s %s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), title))
    # If exception is caught, when editing message (i.e. the message was deleted), assign 0 to message_ID, this will make the bot send new message
    if exception == 'Message':
        message_ID = 0
        if serverstatus.debug == True:
            print("%sResending Message!%s" %(serverstatus.colors('Error'), serverstatus.colors('Normal')))
    # else, just get the messageID from the database
    else:
        message_ID = int(message_ID)
    
    if serverstatus.showSteamConnectionInEmbed == True and db_arr[0][4] != 'Minecraft':
        steamConnect = "Connect: steam://connect/%s:%s" % (serverIP, serverPort)
    else:
        steamConnect = None
    
    embedVar = discord.Embed(title=title, color=discord.Color.from_str('0x' + serverstatus.embedColor), timestamp=timestamp, description = steamConnect)
    # If getServerInfo() was able to query server (i.e. the server is online), this will not be NULL, will send server info
    if server_arr != 'NULL':
        if serverstatus.debug == True:
            print("%sServer Is Online! %s" %(serverstatus.colors('Success'), serverstatus.colors('Normal')))
        embedVar.set_thumbnail(url = serverstatus.thumbnailImage)

        embedVar.add_field(name="Status", value=":green_circle: Online", inline=True)

        if serverstatus.showDirectConnectInEmbed == True:
            embedVar.add_field(name="Connection:", value="`%s:%s`" % (serverIP, serverPort), inline=True)

        if serverstatus.showCurrentPlayersInEmbed == True:
            embedVar.add_field(name="Location:", value=":flag_us: US", inline=True)

        if serverstatus.showGameInEmbed == True:
            embedVar.add_field(name="Game:", value="%s" %serverGame, inline=True)

        if serverstatus.showMapInEmbed == True:
            embedVar.add_field(name="Map:", value="`%s`" %server_arr[1], inline=True)

        if serverstatus.showCurrentPlayersInEmbed == True:
            embedVar.add_field(name="Players:", value="%s/%s" % (server_arr[2], server_arr[3]), inline=True)

        if serverstatus.showPlayerNamesInEmbed == True:
            if serverstatus.debug == True:
                print("%sshowPlayerNamesInEmbed is enabled! %s" %(serverstatus.colors('Success'), serverstatus.colors('Normal')))

            if players_arr != 'NULL':
                players = '\n'.join(players_arr)
                embedVar.add_field(name="Current Players Online:", value="```%s```" % (players), inline=False)

                if serverstatus.debug == True:
                    print("%sCurrent Online Players: \n%s%s" %(serverstatus.colors('Info'), serverstatus.colors('Normal'), players))
            else:
                if serverstatus.debug == True:
                    print("%sNo Players Online! %s" %(serverstatus.colors('Error'), serverstatus.colors('Normal')))

        embedVar.set_footer(text=serverstatus.footerNote, icon_url=serverstatus.footerImage)

        if serverstatus.graphEnabled == True:
            path, peakPlayers, peakTime = serverstatus.graph.plot(x, server_arr[2])
            image = await client.get_channel(1046993046488760430).send(file=discord.File(path))
            imageURL  = image.attachments[0].url

            embedVar.set_image(url=imageURL)

            if serverstatus.deleteImagesInDiscord == True:
                await image.delete()

            os.remove(path)
            
            if serverstatus.showServerPeak == True:
                if peakPlayers > 0:
                    if peakPlayers == 1:
                        embedVar.add_field(name="Server Peak", value="`Server peaked at %s with %s player!`" %(peakTime, peakPlayers), inline=False)
                    else:
                        embedVar.add_field(name="Server Peak", value="`Server peaked at %s with %s players!`" %(peakTime, peakPlayers), inline=False)

    else:
        if serverstatus.debug == True:
            print("%sServer Is Offline!%s" %(serverstatus.colors('Error'), serverstatus.colors('Normal')))

        embedVar = discord.Embed(title=title, color=0xFF0000, timestamp=timestamp)

        embedVar.set_thumbnail(url = serverstatus.thumbnailImage)

        embedVar.add_field(name="Status", value=":red_circle: Offline", inline=True)

        if serverstatus.showDirectConnectInEmbed == True:
            embedVar.add_field(name="Connection:", value="`%s:%s`" % (serverIP, serverPort), inline=True)

        if serverstatus.showCurrentPlayersInEmbed == True:
            embedVar.add_field(name="Location:", value=":flag_us: US", inline=True)

        if serverstatus.showGameInEmbed == True:
            embedVar.add_field(name="Game:", value="%s" %db_arr[0][4], inline=True)

        if serverstatus.showMapInEmbed == True:
            embedVar.add_field(name="Map:", value="`N/A`", inline=True)

        if serverstatus.showCurrentPlayersInEmbed == True:
            embedVar.add_field(name="Players:", value="0/0", inline=True)
        #file = discord.File(None, filename=None)
        #embedVar = discord.Embed(title=serverTitle, color=0xFF0000, timestamp=serverstatus.datetime.now(serverstatus.datetime.utcnow().astimezone().tzinfo), description="<:error:1047015196473962537> This server is either unable to be reached or is in an offline state.")
        embedVar.set_footer(text=serverstatus.footerNote, icon_url=serverstatus.footerImage)

    # if the message_ID = 0, then it is either, a new server or it threw an exception in the check in the else statment
    if message_ID == 0:
        message_ID = await channel_ID.send(embed=embedVar)
        if serverstatus.debug == True:
            print("%sSending New Message to %s!\nNew Message: %s%s" %(serverstatus.colors('Info'), channel_ID, message_ID, serverstatus.colors('Normal')))
        serverstatus.database.submit(message_ID, x)
        return

    else:
        if serverstatus.debug == True:
            print("%sTrying to edit message!%s" %(serverstatus.colors('Info'), serverstatus.colors('Normal')))
        # Try to edit the message, if it's there, edit the message.
        try:
            msg = await channel_ID.fetch_message(message_ID)
            #await msg.edit(embed=embedVar, attachments=[])
            await msg.edit(embed=embedVar)
            if serverstatus.debug == True:
                print("%sSuccess!%s" %(serverstatus.colors('Success'), serverstatus.colors('Normal')))
        except discord.errors.NotFound:
            if serverstatus.debug == True:
                print("%sException Raised!%s" %(serverstatus.colors('Error'), serverstatus.colors('Normal')))
            # if the bot doesn't find the message (i.e. the message was deleted)
            # it will just send a new one and replace the id with the new id
            await send(x, 'Message')

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

timesRun = 1

@client.event
async def on_ready():
    global timesRun
    if serverstatus.debug == True:
        print("%sBot is ready!%s" %(cSuccess, cNormal))
        #await serverstatus.database.query(9)
    while True:
        #try:
            serverstatus.updateConfig()
            index = 0

            # Query database for rows in database
            numOfServers = serverstatus.database.initial()

            while index <= numOfServers - 1:
                if serverstatus.debug == True:
                    print("%s\n#######################################\n#%s                Main                 %s#\n#######################################%s" % (serverstatus.colors('SubTitle'), serverstatus.colors('Normal'), serverstatus.colors('SubTitle'), serverstatus.colors('Normal')))
                if serverstatus.debug == True:
                    print("%sServer Index: %s%s" %(cInfo, cNormal, index))
                # wait(5) is here to prevent Discord from rate limiting the bot, which will force you to wait about 4-5 seconds anyway
                await wait(5)

                await send(index, None)

                index += 1

            if timesRun == 1:
                print("%sServer Status has run %s time since last restart!%s" %(cInfo, timesRun, cNormal))
            else:
                print("%sServer Status has run %s times since last restart!%s" %(cInfo, timesRun, cNormal))

            # Prevents user from using ctrl+c to exit script, you need to wait till after the wait function is done
            await wait(serverstatus.refreshTime)
            timesRun += 1
        #except:
        #    on_ready()


client.run(str(serverstatus.token))