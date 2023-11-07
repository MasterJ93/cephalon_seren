"""
This module contains configuration settings for Cephalon Seren, such as
Discord tokens, database settings, and other constants required
for operation.
"""
# import os

settings = {
    'DISCORD_TOKEN': "", # Use 'os.getenv('DISCORD_TOKEN')' in production.
    'COMMAND_PREFIX': '',
    'ROLE_ID': {
        'OPERATOR': "",
        'DRIFTER': "",
        'ALLIANCE': "",
        'WARLORD': "",
        'CLAN': "",
        'ADMIN': "",
        'MOD': ""
    }
}
