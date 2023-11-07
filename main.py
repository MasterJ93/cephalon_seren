"""
main.py: The entry point for the Cephalon Seren Discord bot.
This module initializes the bot, loads the necessary cogs,
and starts the event loop.
"""
# import discord
# from discord.ext import commands

# def main():
#     """
#     Main function to set up and run the Discord bot.
#     """


# if __name__ == "__main__":
#     main()

# This example requires the 'message_content' intent.

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('your token here')
