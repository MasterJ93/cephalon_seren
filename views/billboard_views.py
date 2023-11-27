"""
Contains views related to commands related to managing billboard ads.
"""

import discord
from discord import Color, Embed, File

from config import settings
from utils import clan_ad_manager, exceptions
from utils.clan_ad_manager import ClanAdKey, ClanAdManager
from utils.helpers import URLParser, ImgDownloader
from utils.messages import clan_ad, misc


class BillboardView(discord.ui.View):
    """
    Create's a view for the clan ad.
    """
    def __init__(self,
                 interaction, ad_manager,
                 clan_emblem=None):
        super().__init__()
        self.interaction = interaction
        self.guild = interaction.guild
        self.member = interaction.user
        self.clan_emblem = clan_emblem
        self.ad_manager = ad_manager
        self.ad_preview = AdPreview(interaction, self, self.ad_manager)

    options = [
        discord.SelectOption(
            label=clan_ad['CLAN_AD_0x0'],
            value='0x0'
        ),
        discord.SelectOption(
            label=clan_ad['CLAN_AD_0x1'],
            value='0x1'
        ),
        discord.SelectOption(
            label=clan_ad['CLAN_AD_0x2'],
            value='0x2'
        )
    ]

    async def load(self):
        """
        Finds the dictionary from the ID. If it can't be found, then it
        creates a new one.
        """
        await self.ad_manager.load_ads()

        try:
            await self.ad_manager.read(user_id=self.member.id)
        except clan_ad_manager.IDNotFoundException:
            print("Can't find ID; will now create one instead.")
            await self.ad_manager.create(self.member.id)

    @discord.ui.button(
        label='Enter Clan Information',
        style=discord.ButtonStyle.blurple)
    async def clan_info_button(self,
                               interaction: discord.Interaction,
                               _button: discord.ui.Button):
        """When the \"Enter Clan Information\" button is selected."""
        await interaction.response.send_modal(
            BillboardClanModal(self.interaction, self, self.ad_manager)
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
        """
        When an option in the \"Clan Recruitment\" dropdown is selected.
        """
        await self.ad_manager.load_ads()
        # Update the temp database.
        print(f'Selection: {select.values[0]}')
        await self.ad_manager.update(self.member.id,
            INVITE_STATUS=select.values[0])

        # Update the ad preview.
        await self.ad_preview.edit_message(
            _content=("Here's the ad preview below. " +
                      "Select \"Post Ad\" when you're ready.")
        )

        # Send message to user, stating it works.
        await interaction.response.send_message(
            content="Preview has been updated.",
            ephemeral=True
        )


    @discord.ui.button(
        label='Post Ad',
        style=discord.ButtonStyle.green,
        disabled=True)
    async def post_ad_button(self,
                             interaction: discord.Interaction,
                             _button: discord.ui.Button):
        """
        When the \"Post Ad\" button is selected.
        """
        # Send a message to the alliance-billboard channel
        # with the embed and action buttons.
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        billboard_channel = guild.get_channel( #type: ignore
                settings['CHANNEL_ID']['ALLIANCE_BILLBOARD'])
        print(f"Alliance billboard: {billboard_channel}")
        _id = self.member.id
        title = await self.ad_manager.read(_id, key=ClanAdKey.NAME)
        description = await self.ad_manager.read(
            _id, key=ClanAdKey.DESCRIPTION
        )
        requirements = await self.ad_manager.read(
            _id, key=ClanAdKey.REQUIREMENTS
        )
        clan_emblem_url = await self.ad_manager.read(
            _id, key=ClanAdKey.CLAN_EMBLEM_URL
        )
        status_code = await self.ad_manager.read(
            _id, key=ClanAdKey.INVITE_STATUS
        )
        invite_status = clan_ad.get(
            f"CLAN_AD_{status_code}"
        )
        color = ""

        # Change the colour depending on the invite status.
        if await self.ad_manager.read(_id,
            key=ClanAdKey.INVITE_STATUS) == '0x0':
            color = Color.green()
        else:
            color = Color.red()

        # Grab the URL from Discord to use as the file to upload to
        # the real post.
        emblem_img = None
        try:
            emblem_img = await ImgDownloader().download(clan_emblem_url)
        except exceptions.RequestFailedException:
            await self.interaction.send(
                content="It looks like something went wrong. We may have "
                "to start again. I'm sorry."
            )
            return

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

        _file = File
        if clan_emblem_url != "" and emblem_img is not None:
            file_name=URLParser().get_file_name(clan_emblem_url)
            _embed.set_thumbnail(
                url=f"attachment://{file_name}"
            )

            _file=File(
                emblem_img, URLParser().get_file_name(url=file_name))
        else:
            clan_emblem_url=None
            _file=None

        await billboard_channel.send(content="\u200B", #type: ignore
            file=_file, #type: ignore
            embed=_embed
        )

        # Delete the message and temp dictionary.
        await self.interaction.delete_original_response()
        await self.ad_manager.load_ads()

    @discord.ui.button(
        label='Cancel',
        style=discord.ButtonStyle.red)
    async def cancel_button(self,
                            _interaction: discord.Interaction,
                            _button: discord.ui.Button):
        """When the \"Cancel\" button is selected."""
        # Delete the message and temp dictionary,
        # cancelling the entire operation.
        await self.interaction.delete_original_response()
        await self.ad_manager.load_ads()

class BillboardClanModal(discord.ui.Modal):
    """
    The modal used to enter the details for the Billboard ad.
    """
    def __init__(self, interaction, view, ad_manager):
        super().__init__(title='Billboard Ad')
        self.interaction = interaction
        self.guild = interaction.guild
        self.member = interaction.user
        self.view = view
        self.ad_preview = AdPreview(interaction, view, ad_manager)
        self.ad_manager = ad_manager

    clan_name = discord.ui.TextInput(
        label="Clan name",
        placeholder='Shinobi of the Lotus',
        custom_id='clan_name',
        min_length=5,
        max_length=100,
        style=discord.TextStyle.short,
        required=True
    )

    clan_description = discord.ui.TextInput(
        label="Write a description of your clan.",
        placeholder=("Shinobi of the Lotus is a clan that helps players be "
            "masters at movement and navigation."),
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
        """
        When the \"Submit\" button is selected.
        """
        # Enable the "Post Ad" message.
        self.view.children[3].disabled = False

        # Retrieve existing values
        ad_json = await self.ad_manager.read(user_id=self.member.id)
        updates = {}

        # Compare and prepare updates
        print(f"Name: {self.clan_name.value} == {ad_json.get('NAME')}\n")
        if self.clan_name.value != ad_json.get('NAME'):
            updates['NAME'] = self.clan_name.value
        print(f"Description: {self.clan_description.value} == {ad_json.get('DESCRIPTION')}\n")
        if self.clan_description.value != ad_json.get('DESCRIPTION'):
            updates['DESCRIPTION'] = self.clan_description.value
        print(f"Requirements: {self.clan_requirements.value} == {ad_json.get('REQUIREMENTS')}\n")
        if self.clan_requirements.value != ad_json.get('REQUIREMENTS'):
            updates['REQUIREMENTS'] = self.clan_requirements.value


        # Update values in dictionary if there are changes
        print('About to update...')
        if updates:
            await self.ad_manager.update(self.member.id, **updates)

        # Update the ad preview.
        await self.ad_preview.edit_message(
            _content=("Here's the ad preview below. " +
                      "Select \"Post Ad\" when you're ready.")
        )

        # Send message to user, stating it works
        # (this is also used to dismiss the modal).
        await interaction.response.send_message(
            content="Preview has been updated.",
            delete_after=10.0,
            ephemeral=True
        )


class AdPreview:
    """
    This is to grab the values and update the clan ad.
    """
    def __init__(self, interaction, view, ad_manager: ClanAdManager):
        self.interaction = interaction
        self.view = view
        self.member = interaction.user
        self.guild = interaction.guild
        self.ad_manager = ad_manager
        self.url_parser = URLParser()
        self.img_downloader = ImgDownloader()

    async def edit_message(self, _content):
        """
        Edits the original message of the ad preview.
        """
        member_id = self.member.id
        clan_ad_details = await self._get_clan_ad_details(member_id)
        color = self._determine_color(
            clan_ad_details[ClanAdKey.INVITE_STATUS]
            )
        emblem_img = await self._download_emblem_image(
            clan_ad_details[ClanAdKey.CLAN_EMBLEM_URL]
            )
        embed = self._build_embed(clan_ad_details, color, emblem_img)
        await self._send_embed(embed, _content)

    async def _get_clan_ad_details(self, member_id):
        keys = [
            ClanAdKey.NAME, ClanAdKey.DESCRIPTION, ClanAdKey.REQUIREMENTS,
            ClanAdKey.CLAN_EMBLEM_URL, ClanAdKey.INVITE_STATUS
            ]
        return {
            key: await self.ad_manager.read(
                member_id, key=key
                ) for key in keys
                }

    def _determine_color(self, invite_status):
        return Color.green() if invite_status == '0x0' else Color.red()

    async def _download_emblem_image(self, url):
        try:
            return await self.img_downloader.download(url)
        except exceptions.RequestFailedException:
            await self.interaction.send(
                content=("It looks like something went wrong. "
                         "We may have to start again. I'm sorry.")
            )
            return None

    def _build_embed(self, details, color, emblem_img):
        # Set up the invite status.
        invite_status_code = details[ClanAdKey.INVITE_STATUS]
        invite_status_description = clan_ad.get(
            f'CLAN_AD_{invite_status_code}', 'Unknown Status'
        )

        # Begin building the Embed.
        embed = Embed(
            title=details[ClanAdKey.NAME],
            description=details[ClanAdKey.DESCRIPTION],
            color=color
        )

        embed.add_field(
            name='Invite Requirements',
            value=details[ClanAdKey.REQUIREMENTS], inline=False)
        embed.add_field(
            name='Invite Status', value=invite_status_description,
            inline=True
            )

        if details[ClanAdKey.CLAN_EMBLEM_URL] and emblem_img:
            file_name = self.url_parser.get_file_name(
                details[ClanAdKey.CLAN_EMBLEM_URL]
                )
            embed.set_thumbnail(url=f"attachment://{file_name}")

        return embed

    async def _send_embed(self, embed, _content):
        await self.interaction.edit_original_response(
            content=_content, embed=embed, view=self.view
            )
