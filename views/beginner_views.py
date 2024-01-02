"""
Contains views related to members that just came into the server.
"""
import asyncio
import discord

from config import settings
from utils.messages import beginner, requests


class OnboardView(discord.ui.View):
    """
    Contains a view for first-time members.
    """
    def __init__(self,
                 user_id: int,
                 alliance_general: discord.TextChannel,
                 alliance_billboard: discord.TextChannel):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.alliance_general = alliance_general
        self.alliance_billboard = alliance_billboard
        self.value = None

    # For whatever reason, putting a "/" in the method stops Pylint
    # from complaining. Hopefully there are no side effects.
    async def interaction_check(self,
                                interaction: discord.Interaction, /) -> bool:
        return interaction.user.id == self.user_id

    @discord.ui.button(
        label=beginner['DROPDOWN_OPTION_1'],
        style=discord.ButtonStyle.green
    )
    async def selection_1(self,
                          interaction: discord.Interaction,
                          button: discord.ui.Button):
        """
        When the first option is selected.
        """
        label = button.label
        print(f"\"{label}\" selected.")

        response_message = beginner['OPTION_1_RESPONSE']

        # Unlike the other options, this option will have Seren send a message
        # to the admins in the admin channel, asking if they want to accept
        # the member's invite.
        admin_channel = self.alliance_billboard.guild.get_channel(
            settings['CHANNEL_ID']['ADMIN_CHANNEL']
        )
        print(f'Alliance General: {self.alliance_billboard.guild}')
        member = self.alliance_billboard.guild.get_member(self.user_id)

        if isinstance(admin_channel, discord.abc.Messageable) and \
            isinstance(member, discord.Member):
            view = ClanInviteInterestView(self.user_id,
                                          self.alliance_general.guild)
            await admin_channel.send(
                content=beginner['INVITE_INTEREST'].format(
                    username=member.mention),
                view=view
            )

        await self.send_message_and_end_onboarding(interaction,
                                                   response_message)

    @discord.ui.button(
        label=beginner['DROPDOWN_OPTION_2'],
        style=discord.ButtonStyle.green
    )
    async def selection_2(self,
                          interaction: discord.Interaction,
                          button: discord.ui.Button):
        """
        When the second option is selected.
        """
        label = button.label
        print(f"\"{label}\" selected.")

        response_message = beginner['OPTION_2_RESPONSE'].format(
                    billboards=self.alliance_billboard.mention
        )

        await self.send_message_and_end_onboarding(interaction,
                                                   response_message)

    @discord.ui.button(
        label=beginner['DROPDOWN_OPTION_3'],
        style=discord.ButtonStyle.green
    )
    async def selection_3(self,
                          interaction: discord.Interaction,
                          button: discord.ui.Button):
        """
        When the third option is selected.
        """
        label = button.label
        print(f"\"{label}\" selected.")

        response_message = beginner['OPTION_3_RESPONSE']

        await self.send_message_and_end_onboarding(interaction,
                                                   response_message)

    async def send_message_and_end_onboarding(
        self,
        interaction: discord.Interaction,
        response_message: str):
        """
        Sends an ephemeral message, then finds and deletes the
        original message.
        """

        # Ephemeral message is sent, then is deleted after a minute.
        await interaction.response.send_message(
            content=response_message,
            ephemeral=True,
            delete_after=60.0
        )

        message_counter = 3
        async for message in \
            interaction.channel.history(limit=200): #type: ignore
            if message.author.bot is True:
                await message.delete()
                await asyncio.sleep(3)
                message_counter -= 1

                if message_counter == 0:
                    break


class ClanInviteInterestView(discord.ui.View):
    """
    Contains a view for admins to decide whether to
    accept or reject a clan invite.
    """
    def __init__(self, user_id: int, guild: discord.Guild):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.guild = guild
        self.value = None

    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green)
    async def accept_invite(self,
                            interaction: discord.Interaction,
                            button: discord.ui.Button):
        """
        When the \"Accept\" button is selected.
        """
        button.disabled=True
        button.style=discord.ButtonStyle.gray

        member = interaction.guild.get_member(self.user_id) #type: ignore
        drifter_role = interaction.guild.get_role( #type: ignore
            settings['ROLE_ID']['DRIFTER']
        )
        clan_role = interaction.guild.get_role( # type: ignore
            settings['ROLE_ID']['CLAN']
        )

        # Add the roles to the new clan member.
        await member.add_roles(drifter_role, clan_role) #type: ignore

        # Send a message stating that it's done.
        await interaction.response.send_message(
            content=beginner['INVITE_ACCEPT']
        )

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_invite(self,
                             interaction: discord.Interaction,
                             button: discord.ui.Button):
        """
        When the \"Decline\" button is selected.
        """
        button.disabled=True
        button.style=discord.ButtonStyle.gray

        # Sends a response back to the admins.
        await interaction.response.send_message(
            content=beginner['INVITE_DECLINE']
        )

    @discord.ui.button(label="Block", style=discord.ButtonStyle.red)
    async def _block_member(self,
                           interaction: discord.Interaction,
                           button: discord.ui.Button):

        # View for blocking and unblocking a user.
        await interaction.response.send_message(
            content=requests['INVITE_USER_BLOCKED'],
            ephemeral=True
        )
