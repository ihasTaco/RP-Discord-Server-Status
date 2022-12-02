import configparser
config = configparser.ConfigParser()

config['TOKEN'] = {
    'botToken': 'Change Me'
}

config['DATABASE'] = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'table': 'server_info',
    'database': 'servers'
}

#############################################################################################################################################
#                                                                   LEGEND                                                                  #
#############################################################################################################################################
# Strings | 'Anything That you put in between two '' or "" '                                                                                #
#   - While everything in this config is a string, I am using them as I specify Boolean will be treated as a Bool, Integer as an int, etc.  #
# Boolean | True or False                                                                                                                   #
#   - If you put anything but True or False, it will be treated as False (even true **MAKE SURE YOU CAPITALIZE THE T AND F**)               #
# Integer | 100, 0, -50, 102378265278 are all integers.                                                                                     #
#                                                                                                                                           #
# Float   | 100.00, 0.25, -50.1224, 102378265278.7e100 are all floats                                                                       #
#   - There shouldn't be any floats in this script but just in case I add something that requires it                                        #
#############################################################################################################################################

config['GENERAL'] = {
    # Boolean
    # True will print a bunch of information in the console, not really needed unless something isn't working
    'debugMode': 'True',
    # Integer (in Seconds)
    # How long should the script wait to refresh the server info
    'refreshTime': '60',
    # String
    # This will be a URL, if you don't have a domain to host it on, you can upload it to any image sharing platform (imgur)
    # and copy past the embed link here!
    # Or, if it's going to be your Discord server icon, you can get your image link
    # Here's a reddit post about it: https://www.reddit.com/r/discordapp/comments/ch6v29/how_to_download_a_discord_servers_iconimage/
    # Your Discord image link will look something like: https://cdn.discordapp.com/icons/360541835371741185/201c015115ff6e8352486a8ad6c39a1a.webp
    # While I haven't researched it I know that you *SHOULD* be able to use local images with the API, but I don't know if that will require
    # some change to the code
    # IF YOU DON'T WANT TO USE THIS, DELETE THE URL,
    'thumbnailImage': 'https://royalproductions.xyz/images/logo/RP_Logo_Outline.png',
    # String
    # This will be a HEX Color
    # If you don't know what that is:
    # https://www.google.com/search?q=hex+color+picker&oq=hex+color&aqs=chrome.1.69i59l2j69i60.3293j0j1&sourceid=chrome&ie=UTF-8
    # Follow that link, it will open on google a color picker, under the colors it will give you HEX, RGB, CMYK, HSV, and HSL
    # But the script can only handle HEX values so just copy and paste that here
    'embedColor': 'ff7d00',
    # Boolean
    # If set to True, titles will use title of server, and may result in names like '90166394542026753' or 'DieDieDie' for instance
    # If set to False, embed titles will use the 'Server Name' in database
    'useServerNameAsTitle': 'False',
    # Boolean
    # If True, These specific fields will be enabled and show up in the embed
    # If False, These specific fields will be disabled and will not show up in embed
    'showDirectConnectInEmbed': 'True',
    'showGameInEmbed': 'False',
    'showMapInEmbed': 'True',
    'showCurrentPlayersInEmbed': 'True',
    'showSteamConnectionInEmbed': 'False',
    'showPlayerNamesInEmbed': 'True',
    # Boolean
    # If set to True, embed will grab machine local time and display it (i.e. Today at 9:49 AM)
    'showTimeStamp': 'True',
    # String
    # This allows you to set a note on the footer of the embed!
    # p.s. if you want to embed an emoji do \:emoji_name: in discord (NOTE THE BACKSLASH '\' NOT FORWARDSLASH '/')
    # this will give you something like '<:emoji_name:1234567890123456789>', put all of that in between the ''!
    # IF YOU DON'T WANT TO USE THIS, DELETE EVERYTHING IN THE STRING 
    'footerNote': 'Game Status by Royal Productions',
    # String
    # This will be a URL
    # (look at thumbnailImage if you need help)
    # IF YOU DON'T WANT TO USE THIS, DELETE THE URL
    'footerImage': 'https://cdn.discordapp.com/icons/360541835371741185/201c015115ff6e8352486a8ad6c39a1a.webp',
}


###### DO NOT MESS WITH ANYTHING PAST HERE ######
with open('config.ini', 'w') as configfile:
    config.write(configfile)

print('\033[1;32mConfig Updated!\033[1;00m')