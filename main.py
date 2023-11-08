"""
main.py: The entry point for the Cephalon Seren Discord bot.
This module initializes the bot, loads the necessary cogs,
and starts the event loop.
"""
import discord
from discord.ext import commands
from config import settings

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=settings['COMMAND_PREFIX'],
                   intents=intents)

@bot.event
async def on_ready():
    """
    Called when the bot is ready.
    """
    await bot.tree.sync()

    print("Successfully connected to Discord.")

def main():
    """
    Main function to set up and run the Discord bot.
    """
    initial_extensions = [
        'cogs.membership'
    ]

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception:
            print(f'Failed to load extension: ({extension}).')

    bot.run(settings['DISCORD_TOKEN'])


if __name__ == "__main__":
    main()
