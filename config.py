"""
This module contains configuration settings for Cephalon Seren, such as
Discord tokens, database settings, and other constants required
for operation.
"""
# import os

settings = {
    'DISCORD_TOKEN': "", # Use 'os.getenv('DISCORD_TOKEN')' in production.
    'COMMAND_PREFIX': '/',
    'ROLE_ID': {
        'OPERATOR': "1066899336212004887",
        'DRIFTER': "1066899404688207892",
        'ALLIANCE': "1066969325581381672",
        'WARLORD': "1169338858375237732",
        'CLAN': "1066969178461970494",
        'ADMIN': "885275629497499694",
        'CLAN_MOD': "1066898095364915230",
        'ALLIANCE_MOD': "1066899219828457512"
    }
}
