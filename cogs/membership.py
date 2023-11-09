"""
membership.py: A discord.py cog for Cephalon Seren that manages server
membership features, such as assigning roles to new members and sending
them a message to inquire about their interest in joining the clan.
"""
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from config import settings

class Membership(commands.Cog):
    """
    Membership Cog for handling new members and their roles.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener
    async def on_member_join(self, member):
        """
        Event listener for when a member joins the server.
        Assigns roles after a delay and sends a message to the member.
        """

        # Wait for a set amount of time before assigning the role
        await asyncio.sleep(5)

        await member.add_roles(settings['ALLIANCE'],
                               settings['OPERATOR'])
