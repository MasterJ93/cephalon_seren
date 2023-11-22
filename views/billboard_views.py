"""
Contains views related to commands related to managing billboard ads.
"""

import discord
from discord import Color, Embed
from utils.clan_ad_manager import ClanAdKey, ClanAdManager

class BillboardView(discord.ui.View):
    """docstring for BillboardView."""
    def __init__(self,
                 interaction,
                 clan_emblem=None):
        super().__init__()
        self.interaction = interaction
        self.guild = interaction.guild
        self.member = interaction.user
        self.clan_emblem = clan_emblem

    options = [
        discord.SelectOption(
            label="We're currently accepting invite requests."
        ),
        discord.SelectOption(
            label="We're not accepting invite requests right now."
        ),
        discord.SelectOption(
            label="We currently can't add any new members."
        )
    ]

    @discord.ui.button(
        label='Enter Clan Information',
        style=discord.ButtonStyle.blurple)
    async def clan_info_button(self,
                               interaction: discord.Interaction,
                               _button: discord.ui.Button):
        """When the \"Enter Clan Information\" button is selected."""
        await interaction.response.send_modal(
            BillboardClanModal(self.interaction, self)
        )

    @discord.ui.button(
        label='Upload Clan Emblem',
        style=discord.ButtonStyle.blurple)
    async def upload_clan_emblem(self,
                                 interaction: discord.Interaction,
                                 _button: discord.ui.Button):
        """When the \"Upload Clan Emblem\" button is selected."""
        # Inform the member how to upload the clan emblem.
        await interaction.response.send_message(
            content=misc['UPLOAD_EMBLEM'],
            ephemeral=True
        )


    @discord.ui.select(
        placeholder='Select invite status',
        custom_id='clan_inv',
        options=options
    )
    async def clan_invite_dropdown(self,
                                   interaction: discord.Interaction,
                                   select: discord.ui.Select):
        """When an option in the \"Clan Recruitment\" dropdown is selected."""

    @discord.ui.button(
        label='Post Ad',
        style=discord.ButtonStyle.green,
        disabled=True)
    async def post_ad_button(self,
                             interaction: discord.Interaction,
                             button: discord.ui.Button):
        """When the \"Post Ad\" button is selected."""

    @discord.ui.button(
        label='Cancel',
        style=discord.ButtonStyle.red)
    async def cancel_button(self,
                            _interaction: discord.Interaction,
                            _button: discord.ui.Button):
        """When the \"Cancel\" button is selected."""
        # Delete the message, cancelling the entire operation.
        await self.interaction.delete_original_response()

class BillboardClanModal(discord.ui.Modal):
    """The modal used to enter the details for the Billboard ad."""
    def __init__(self, interaction, view):
        super().__init__(title='Billboard Ad')
        self.interaction = interaction
        self.guild = interaction.guild
        self.member = interaction.user
        self.view = view

    clan_name = discord.ui.TextInput(
        label="Clan name (3-digits after \"#\")",
        placeholder='Shinobi of the Lotus#141',
        custom_id='clan_name',
        min_length=5,
        max_length=100,
        style=discord.TextStyle.short,
        required=True
    )

    clan_description = discord.ui.TextInput(
        label="Write a description of your clan.",
        placeholder="Shinobi of the Lotus is a clan that helps players be "\
            "masters at movement and navigation.",
        custom_id='clan_des',
        max_length=1024,
        style=discord.TextStyle.long,
        required=False
    )

    clan_requirements = discord.ui.TextInput(
        label="Set the requirements of your clan.",
        placeholder="We require members to be 18 or older.",
        custom_id='clan_req',
        max_length=300,
        style=discord.TextStyle.long,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction, /):
        """When the \"Submit\" button is selected."""
        # Edit main message.
        self.view.children[3].disabled = False

        # Build the embed.
        embed = Embed(
            title=f"{self.clan_name.value}",
            description=self.clan_description.value,
            color=Color.red()
        )
        embed.add_field(
            name='Invite Requirements',
            value=self.clan_requirements.value,
            inline=False
        )
        embed.add_field(
            name="We're not taking new members.",
            value="\u200B",
            inline=True
        )
        await self.interaction.edit_original_response( #type: ignore
            content='It works!',
            embed=embed,
            view=self.view
        )

        # Send message to user, stating it works
        # (this is also used to dismiss the modal).
        await interaction.response.send_message(
            content="Information has been updated.",
            ephemeral=True
        )


class AdPreview():
    """This is to grab the values and update the clan ad."""
    def __init__(self, interaction, view):
        super().__init__()
        self.interaction = interaction
        self.view = view
        self.member = interaction.user
        self.guild = interaction.guild
        self.manager = ClanAdManager(self.member.id)

    async def edit_message(self, _content="", _ephemeral=True):
        """
        Edits the original message of the ad preview.
        """
        title = self.manager.read(ClanAdKey.NAME)
        description = self.manager.read(ClanAdKey.DESCRIPTION)
        requirements = self.manager.read(ClanAdKey.REQUIREMENTS)
        clan_emblem_url = self.manager.read(ClanAdKey.CLAN_EMBLEM_URL)
        invite_status = self.manager.read(ClanAdKey.INVITE_STATUS)
        color = ""

        # Change the colour depending on the invite status.
        if self.manager.read(ClanAdKey.INVITE_STATUS) == '0x0':
            color = Color.green()
        else:
            color = Color.red()

        # Build the embed.
        _embed = Embed(
            title=title,
            description=description,
            color=color
        )
        _embed.add_field(
            name='Invite Requirements',
            value=requirements,
            inline=False
        )
        _embed.add_field(
            name=invite_status,
            value="\u200B",
            inline=True
        )

        await self.interaction.response.edit_original_response(
            content=_content,
            embed=_embed,
            ephemeral=_ephemeral
        )
