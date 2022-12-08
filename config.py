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
    'refreshTime': '10',
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
    # NOTE: This will also be used for the player graph!
    'embedColor': 'ff7d00',
    # Boolean
    # If set to True, titles will use title of server, and may result in names like '90166394542026753' or 'DieDieDie' for instance
    # If set to False, embed titles will use the 'Server Name' in database
    'useServerNameAsTitle': 'False',
    # Boolean
    # If True, These specific fields will be enabled and show up in the embed
    # If False, These specific fields will be disabled and will not show up in embed
    'showDirectConnectInEmbed': 'True',
    'showGameInEmbed': 'True',
    'showMapInEmbed': 'True',
    'showCurrentPlayersInEmbed': 'True',
    'showPlayerGraph': 'True',
    'showSteamConnectionInEmbed': 'True',
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

config['GRAPH'] = {
    ##########################################
    #         Player Graph Settings          #
    ##########################################
    # Enable/Disable Player Graphs, This will also disable peak hour message in embed!
    'graphEnabled': 'True',                        # Default: True
    'graphTitle': '',                              # Default: ''
    'graphLabel': 'Online Players',                # Default: 'Online Players'
    'graphXLabel': '',                             # Default: ''
    'graphYLabel': 'Players',                      # Default: 'Players'

    # Int
    # This is going to be used to send player graph images to discord
    # Due to limitations to discord.py you can't edit embed images with local files.
    # I figured the best way to do this is to send the images to an empty channel (perferrably one that not many have access to),
    # get the link to the image, display it in the embed and then delete the image in discord as well as from the images folder
    'discordImageChannel': '1046993046488760430',                    # Default: ''

    # String
    # If you don't want to use the embed color for the graphs, then set it here, else keep it empty
    'graphColor': '',                             # Default: ''
    
    # Boolean
    # Adds a feild in the embed that says something like 'Server peaked at x AM/PM with y player(s)!'
    # Server Peak will only show if there were more than 0 players in the server since the script started running
    'showServerPeak': 'True',

    # Boolean
    # This setting is, in my opinion, kinda controversial, I personally dont want to clutter an entire channel with images
    # But I noticed a bug, where if you are deleting all the images, almost as soon as your uploading them,
    # I noticed that if the user client (discord) hasn't cached the images, they will keep loading the image and never
    # show until the server is queried and an image is uploaded again.
    # Because of this the default will be 'False', if you can deal with this, then turn it True
    'deleteImagesInDiscord': 'False',

    # GRAPH OPACITY SETTINGS 

    # Float
    # These will all be floats ranging between 0.0 - 1.0, if they go over/under 1/0, an error will be raised!
    # if you want to turn any of these off just set the float to 0.0, and they will turn transparent
    'graphBorderTopOpacity': '0.0',              # Default: 0.0
    'graphBorderBottomOpacity': '0.5',           # Default: 0.5
    'graphBorderLeftOpacity': '0.5',             # Default: 0.5
    'graphBorderRightOpacity': '0.0',            # Default: 0.0
    'graphXAxisLabelOpacity': '0.5',             # Default: 0.5
    'graphYAxisLabelOpacity': '0.5',             # Default: 0.5
    'graphTitleOpacity': '0.0',                  # Default: 0.5
    'graphXLabelOpacity': '0.5',                 # Default: 0.5
    'graphYLabelOpacity': '0.0',                 # Default: 0.5
    # The Graph Fill is the color between 0 and the Online Players Line
    'graphFillOpacity': '0.25',                  # Default: 0.25
}

###### DO NOT MESS WITH ANYTHING PAST HERE ######
with open('config.ini', 'w') as configfile:
    config.write(configfile)

print('\033[1;32mConfig Updated!\033[1;00m')