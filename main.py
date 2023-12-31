"""
The entry point for the Cephalon Seren Discord bot.
This module initializes the bot, loads the necessary cogs,
and starts the event loop.
"""
import asyncio
import logging

import discord
from discord.ext import commands

from cogs.admin import AdminCommands
from cogs.billboard import BillBoardCommands
from cogs.membership import Membership
from config import settings
from utils.clan_ad_manager import ClanAdManager

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix=settings['COMMAND_PREFIX'],
                   intents=intents)

# Create a shared instance of ClanAdManager
clan_ad_manager = ClanAdManager()

@client.event
async def on_ready():
    """
    Called when the bot is ready.
    """
    await clan_ad_manager.load_ads()
    print('Success!')
    logger.info("Successfully connected to Discord.")

@client.tree.command(name='ping',
                     description='Sends the bot\'s '
                     'frequency in milliseconds (ms).')
async def ping(interaction: discord.Interaction):
    """
    Sends the bot's frequency in milliseconds (ms).
    """
    await interaction.response.send_message(
        f"Pong! ({round(client.latency * 1000)}ms)")

@client.command()
async def sync(_ctx):
    """
    Syncs the global commands.
    """
    try:
        command_list = await client.tree.sync()
        command_names = [command.name for command in command_list]
        print(f'Commands: {command_names}')

        print('Commands have been synced.')
    except discord.DiscordException as err:
        print(err)

initial_cogs = [
    Membership(client, clan_ad_manager),
    AdminCommands(client),
    BillBoardCommands(client, clan_ad_manager)
]

for cog in initial_cogs:
    try:
        asyncio.run(client.add_cog(cog))
        print(f'Successfully added cog: {cog.qualified_name}.')
        logger.info("%s has been successfully added.", cog)
    except discord.DiscordException as e:
        print(e)


client.run(settings['DISCORD_TOKEN'],
        #    root_logger=False
           )
