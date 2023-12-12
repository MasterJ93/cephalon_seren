"""
Contains views related to requests made by members.
"""
import discord

from config import settings
from utils.clan_ad_manager import ClanAdKey, ClanAdManager
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

        self._selected_clan = []


    options = []

    async def refresh_clan_invite_list(self, clan_list):
        """
        Loops through all of the clans that are open for members.

        Args:
            clan_list (list[dict]): The list of clans.
        """
        # Clear the options:
        self.options.clear()

        counter = 0
        for clan in clan_list:
            clan_name = clan.get(ClanAdKey.NAME)
            clan_option = discord.SelectOption(
                label=clan_name,
                value=str(counter)
            )

            self.options.append(clan_option)
            counter += 1

    @discord.ui.select(
            placeholder='Select a clan.',
            min_values=1,
            max_values=1,
            options=options)
    async def _rule_selection(self,
                             interaction: discord.Interaction,
                             select: discord.ui.Select):
        # Convert the string to an integer index, then use the
        # index to access the item in clan_list
        index = int(select.values[0])
        self._selected_clan = self.clan_list[index]

        self.children[1].disabled = False #type: ignore


    @discord.ui.button(
        label='Request Invite',
        style=discord.ButtonStyle.green,
        disabled=True,
        custom_id='request_invite'
    )
    async def _request_invite(self,
                             interaction: discord.Interaction,
                             _button: discord.ui.Button):
        await self.ad_manager.load_ads()

        warlord_id = list(self._selected_clan.keys())[0] #type: ignore
        warlord_id = self.ad_manager.read(int(warlord_id))

        # There may be a chance a Warlord closes their doors while the
        # user is requesting the invite. In that case, inform the user.
        if self.ad_manager.read(
            warlord_id, ClanAdKey.INVITE_STATUS) != '0x0':
            await interaction.response.edit_message(
                content=requests['CLAN_INVITE_TOO_LATE']
            )
            return

        # Send a DM to the Warlord.
        warlord = discord.utils.get(
            interaction.guild.members, id=warlord_id # type: ignore
            )
        if warlord.dm_channel is None: #type: ignore
            await warlord.create_dm() #type: ignore

        await warlord.dm_channel.send( #type: ignore
            content=''
        )

        await interaction.response.edit_message(
            content=requests['INVITE_INTEREST_SENT']
        )


    @discord.ui.button(
        label='Cancel',
        style=discord.ButtonStyle.red,
        disabled=True,
        custom_id='cancel'
    )
    async def _cancel_button(self,
                             interaction: discord.Interaction,
                             _button: discord.ui.Button):
        await interaction.delete_original_response()
