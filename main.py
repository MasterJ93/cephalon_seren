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


if __name__ == "__main__":
    main()

# import discord

# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

# client.run('your token here')
