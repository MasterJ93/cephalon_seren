"""
main.py: The entry point for the Cephalon Seren Discord bot.
This module initializes the bot, loads the necessary cogs,
and starts the event loop.
"""
import logging
import discord
from discord.ext import commands
from config import settings

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=settings['COMMAND_PREFIX'],
                   intents=intents)

@client.event
async def on_ready():
    """
    Called when the bot is ready.
    """
    await client.tree.sync()

    logger.info("Successfully connected to Discord.")

@client.tree.command(name='ping',
                     description='Sends the bot\'s '\
                     'frequency in milliseconds (ms).')
async def ping(interaction: discord.Interaction):
    """
    Sends the bot's frequency in milliseconds (ms).
    """
    await interaction.response.send_message(
        f"Pong! ({round(client.latency * 1000)}ms)")

def main():
    """
    Main function to set up and run the Discord bot.
    """
    initial_extensions = [
        'cogs.membership'
    ]

    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except discord.DiscordException:
            print(f'Failed to load extension: ({extension}).')

    client.run(settings['DISCORD_TOKEN'])


if __name__ == "__main__":
    main()
