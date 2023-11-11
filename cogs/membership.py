"""
membership.py: A discord.py cog for Cephalon Seren that manages server
membership features, such as assigning roles to new members and sending
them a message to inquire about their interest in joining the clan.
"""
import asyncio
from discord.ext import commands
from config import settings

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

        # Post an ephemeral message, asking the member if they're here to
        # join the clan.
        channel = member.guild.get_channel(
            # settings['CHANNEL_ID']['ALLIANCE_GENERAL']
            1172080684672749568
            )
        webhooks = await channel.webhooks()
        print(webhooks)
        seren_webhook = webhooks[0]

        await seren_webhook.send(content='It works!')
