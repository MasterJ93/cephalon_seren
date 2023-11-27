"""
This module contains configuration settings for Cephalon Seren, such as
Discord tokens, database settings, and other constants required
for operation.
"""
import os

settings = {
    'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN'),
    'COMMAND_PREFIX': os.getenv('COMMAND_PREFIX'),
    'ROLE_ID': {
        'RULES': int(os.getenv('RULES', '0')),
        'OPERATOR': int(os.getenv('OPERATOR', '0')),
        'DRIFTER': int(os.getenv('DRIFTER', '0')),
        'ALLIANCE': int(os.getenv('ALLIANCE', '0')),
        'WARLORD': int(os.getenv('WARLORD', '0')),
        'CLAN': int(os.getenv('CLAN', '0')),
        'ADMIN': int(os.getenv('ADMIN', '0')),
        'CLAN_MOD': int(os.getenv('CLAN_MOD', '0')),
        'ALLIANCE_MOD': int(os.getenv('ALLIANCE_MOD', '0'))
    },
    'CHANNEL_ID': {
        'ALLIANCE_GENERAL': int(os.getenv('ALLIANCE_GENERAL', '0')),
        'ADMIN_CHANNEL': int(os.getenv('ADMIN_CHANNEL', '0')),
        'CLAN_GENERAL': int(os.getenv('CLAN_GENERAL', '0')),
        'REPORTS_APPEALS': int(os.getenv('REPORTS_APPEALS', '0')),
        'ALLIANCE_BILLBOARD': int(os.getenv('ALLIANCE_BILLBOARD', '0'))
    }
}
