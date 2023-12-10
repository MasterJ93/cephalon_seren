"""
Contains views related to requests made by members.
"""
import discord

from config import settings
from utils.clan_ad_manager import ClanAdManager
from utils.messages import requests


class DrifterInterestView(discord.ui.View):
    """
    Contains a view for admins to consider adding a member to participate
    in the adult-only channels.
    """
    def __init__(self, user_id, guild: discord.Guild):
        super().__init__(timeout=None)
        self.user_id=user_id
        self.guild=guild
        self.value=None

    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green)
    async def accept_request(self,
                             interaction: discord.Interaction,
                             button: discord.ui.Button):
        """
        If the \"Accept\" button was selected.
        """
        button.disabled=True
        button.style=discord.ButtonStyle.gray

        member = self.guild.get_member(self.user_id)
        drifter_role = self.guild.get_role(
            settings['ROLE_ID']['DRIFTER']
        )

        # Add the role to the member.
        if isinstance(member, discord.Member) and \
            isinstance(drifter_role, discord.Role):
            await member.add_roles(drifter_role)

        # Sends a message in the admin channel, stating that it's done.
        await interaction.response.send_message(
            content=requests['DRIFTER_ACCEPT']
        )

    @discord.ui.button(label='Decline', style=discord.ButtonStyle.red)
    async def reject_request(self,
                             interaction: discord.Interaction,
                             button: discord.ui.Button):
        """
        If the \"Decline\" button was selected.
        """
        print(f'\"{button.label}\" button pressed.')
        button.disabled=True
        button.style=discord.ButtonStyle.gray

        # Sends a message to the admin channel, stating it will be declined.
        await interaction.response.send_message(
            content=requests['DRIFTER_DECLINE']
        )

class ClanInviteRequestView(discord.ui.View):
    """
    Contains a view for users to select a clan that's open for invites.
    """
    def __init__(self, user_id, clan_list, ad_manager: ClanAdManager):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.clan_list = clan_list
        self.ad_manager = ad_manager

        # Loop through all of the clans.
        for clan in clan_list:
            clan_option = discord.SelectOption(
                label='[Name of clan]'
            )
            self.options.append(clan_option)


    options = []

    @discord.ui.select(
            placeholder='Select a clan.',
            min_values=1,
            max_values=1,
            options=options)
    async def rule_selection(self,
                             interaction: discord.Interaction,
                             select: discord.ui.Select):
        """
        The dropdown menu that shows the list of clans that are
        open for invites.
        """
        