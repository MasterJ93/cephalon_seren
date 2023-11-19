"""
Contains views related to commands related to managing billboard ads.
"""

import discord

class BillboardView(discord.ui.View):
    """docstring for BillboardView."""
    def __init__(self,
                 guild,
                 member):
        super().__init__()
        self.guild = guild
        self.member = member

    @discord.ui.button(
        label='Enter Clan Information',
        style=discord.ButtonStyle.blurple)
    async def clan_info_button(self,
                               interaction: discord.Interaction,
                               button: discord.ui.Button):
        """When the \"Enter Clan Information\" button is selected."""
        await interaction.response.send_modal(
            BillboardClanModal(
                self.guild,
                self.member
            )
        )

    @discord.ui.button(
        label='Upload Clan Emblem',
        style=discord.ButtonStyle.blurple)
    async def upload_clan_emblem(self,
                                 interaction: discord.Interaction,
                                 button: discord.ui.Button):
        """When the \"Upload Clan Emblem\" button is selected."""

    @discord.ui.button(
        label='Post Ad',
        style=discord.ButtonStyle.red)
    async def post_ad_button(self,
                             interaction: discord.Interaction,
                             button: discord.ui.Button):
        """When the \"Post Ad\" button is selected."""

    @discord.ui.button(
        label='Cancel',
        style=discord.ButtonStyle.red)
    async def cancel_button(self,
                            interaction: discord.Interaction,
                            button: discord.ui.Button):
        """When the \"Cancel\" button is selected."""


class BillboardClanModal(discord.ui.Modal):
    """The modal used to enter the details for the Billboard ad."""
    def __init__(self, guild, member):
        super().__init__(title='Billboard Ad')
        self.guild = guild
        self.member = member

     # This is to allow `clan_invite` to access this variable.
    options = [
        discord.SelectOption(
            label="We're not accepting clan invites right now."
        ),
        discord.SelectOption(
            label="We're currently accepting invites."
        ),
        discord.SelectOption(
            label="We currently can't add any new members."
        )
    ]

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

    # clan_invite = discord.ui.Select(
    #     custom_id='clan_inv',
    #     options=options
    # )

    async def on_submit(self, interaction: discord.Interaction, /):
        """When the \"Submit\" button is selected."""
