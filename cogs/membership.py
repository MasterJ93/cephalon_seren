"""
membership.py: A discord.py cog for Cephalon Seren that manages server
membership features, such as assigning roles to new members and sending
them a message to inquire about their interest in joining the clan.
"""
import asyncio
from discord.ext import commands
from utils.messages import beginner
from config import settings
from views.beginner_views import OnboardView

class Membership(commands.Cog):
    """
    Membership Cog for handling new members and their roles.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Event listener for when a member joins the server.
        Assigns roles after a delay and sends a message to the member.
        """

        # Wait for a set amount of time before assigning the role.
        await asyncio.sleep(5)

        alliance_role = member.guild.get_role(
            settings['ROLE_ID']['ALLIANCE']
        )
        operator_role = member.guild.get_role(
            settings['ROLE_ID']['OPERATOR']
        )
        # Add the Alliance and Operator roles for the member.
        await member.add_roles(alliance_role, operator_role)

        # If a bot was invited into the server, we don't need to give it
        # any messages.
        if member.bot is True:
            return
        # Post an ephemeral message, asking the member if they're here to
        # join the clan.
        channel = member.guild.get_channel(
            settings['CHANNEL_ID']['ALLIANCE_GENERAL']
        )

        # Sends the message and mentions the member.
        # Note: we send alliance_billboard in case the member selects
        # the second option.
        alliance_billboard = member.guild.get_channel(
            settings['CHANNEL_ID']['ALLIANCE_BILLBOARD']
        )
        view = OnboardView(member.id, alliance_billboard)
        await channel.send(
            content=beginner['INTRO'].format(username=member.mention),
            view = view
        )
