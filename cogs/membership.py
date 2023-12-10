"""
A cog for Cephalon Seren that manages server membership features,
such as assigning roles to new members and sending them a message 
to inquire about their interest in joining the clan.
"""
import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from utils.clan_ad_manager import ClanAdKey, ClanAdManager
from utils.messages import beginner, requests
from views.beginner_views import OnboardView
from views.request_views import (
    ClanInviteRequestView, DrifterInterestView
)


class Membership(commands.Cog):
    """
    Membership Cog for handling new members and their roles.
    """
    def __init__(self, bot, ad_manager: ClanAdManager):
        self.bot = bot
        self.ad_manager = ad_manager

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Event listener for when a member joins the server.
        Assigns roles after a delay and sends a message to the member.
        """

        # Wait for a set amount of time before assigning the role.
        await asyncio.sleep(3)

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

        # Sends the message and mentions the member.
        # Note: we send alliance_billboard in case the member selects
        # the second option.
        alliance_billboard = member.guild.get_channel(
            settings['CHANNEL_ID']['ALLIANCE_BILLBOARD']
        )
        channel = await member.create_dm()
        view = OnboardView(member.id, channel, alliance_billboard)
        await channel.send(
            content=beginner['INTRO'].format(username=member.mention),
            view = view
        )

    @app_commands.command(
            name='invite-request',
            description='Request to join a clan.'
    )
    async def invite_request(self,
                             interaction: discord.Interaction,
                             ):
        """
        Requests a Warlord to be part of their clan.
        """
        clan_list = []
        for ad in self.ad_manager.clan_ads:
            if ad.get(ClanAdKey.MESSAGE_ID) == '0':
                continue

            clan_list.append(ad)

        # Change the message based on the total number of
        # openly invited clans.
        if clan_list.count is not 0:
            content = 'Select from the list of clans below:'
            view = ClanInviteRequestView(
                interaction.user.id, clan_list, self.ad_manager
            )
            delete_after = None
        else:
            content = ('Bummer: it seems like none of the clans can take '
                       'any more members. Hopefully a clan may open more '
                       'spots in the future.')
            view = discord.ui.View()
            delete_after = 10

        await interaction.response.send_message(
            content=content,
            view=view,
            ephemeral=True,
            delete_after=delete_after
        )

    @app_commands.command(name='drifter-request',
                          description='Request access to enter into '
                          'the adult-only channels.')
    async def drifter_request(self, interaction: discord.Interaction):
        """
        Requests access to enter into the adult-only channels.
        """

        # Sends a request to access the clan channels as an adult
        # (instead of a a clan member).
        admin_channel = interaction.guild
        if isinstance(admin_channel, discord.Guild):
            admin_channel = admin_channel.get_channel(
                settings['CHANNEL_ID']['ADMIN_CHANNEL']
                )
        if isinstance(admin_channel, discord.TextChannel):
            content=requests['DRIFTER_INTEREST'].format(
                username=interaction.user.mention
            )

            view = DrifterInterestView(
                interaction.user.id, interaction.guild) #type: ignore
            await admin_channel.send(
                content=content,
                view=view
            )

        # Sends an ephemeral message, stating that the user's request has
        # been sent.
        await interaction.response.send_message(
            content=requests['DRIFTER_REQUEST'],
            ephemeral=True
        )

    @app_commands.command(name='operator-request',
                          description='Adds or removes the Operator role '
                          'which adds or removes the alliance channels.'
                          )
    @app_commands.checks.has_role(settings['ROLE_ID']['DRIFTER'])
    async def operator_request(self, interaction: discord.Interaction):
        """
        Requests to add or remove the alliance-only channels.
        """
        # Pylance will complain that some of these things are of type
        # "None," which is incorrect. "# type: ignore"
        # will be used to stop it from lying to us.

        # Grabs the member from the guild.
        guild = interaction.guild
        operator_role=guild.get_role(  # type: ignore
            settings['ROLE_ID']['OPERATOR']
        )
        member=guild.get_member(interaction.user.id)  # type: ignore
        roles=member.roles  # type: ignore

        # Check if the member has the "Operator" role.
        # If yes, then remove the role.
        # If no, then add it.

        if operator_role in roles:
            await member.remove_roles(operator_role) # type: ignore

            await interaction.response.send_message(
                content=requests['OPERATOR_REMOVE'].format(
                    role=operator_role  # type: ignore
                    ),
                    ephemeral=True
            )

        elif operator_role not in roles:
            await member.add_roles(operator_role)  # type: ignore

            await interaction.response.send_message(
                content=requests['OPERATOR_ADD'].format(
                    role=operator_role  # type: ignore
                ),
                ephemeral=True
            )
