import configparser
config = configparser.ConfigParser()

config['TOKEN'] = {
    'botToken': 'Change Me'
}

config['DATABASE'] = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'server_info',
    'table': 'servers'
}

config['GENERAL'] = {
    # True or False
    # True will print a bunch of information in the console, not really needed unless something isn't working
    'debugMode': 'False',
    # refreshTime in Seconds.
    # How long should the script wait to refresh the server info
    'refreshTime': '60',
    # If set to True, titles will use title of server, and may result in names like '90166394542026753' or 'DieDieDie' for instance
    # If set to False, embed titles will use the 'Game Name' in database
    'useServerNameAsTitle': 'True',
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)

print('\033[1;32mConfig Updated!\033[1;00m')