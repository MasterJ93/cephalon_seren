"""
A list of commands related to managing ads in the
alliance-billboard channel.
"""

from typing import Optional

import discord
from discord import Color, Embed, app_commands
from discord.ext import commands

from config import settings
from utils.clan_ad_manager import ClanAdKey, ClanAdManager, \
    IDNotFoundException
from utils.messages import clan_ad
from views.billboard_views import BillboardView


class BillBoardCommands(commands.Cog):
    """
    BillboardCommands Cog for handling billboard ad management.
    """
    def __init__(self, bot, ad_manager: ClanAdManager):
        self.bot = bot
        self.ad_manager = ad_manager

    @app_commands.command(name="billboard")
    @app_commands.describe(
        select='What would you like to do?',
        clan_emblem='Upload a clan emblem to a billboard ad. ' \
            '128x128px, .png/.jpg recommended.'
        )
    @app_commands.choices(select=[
            app_commands.Choice(
                name="Create Ad", value="create"),
            app_commands.Choice(
                name='Edit Ad', value="edit")
    ])
    @app_commands.checks.has_any_role(
        settings['ROLE_ID']['WARLORD'],
        settings['ROLE_ID']['ADMIN'])
    async def billboard_command(self,
                                interaction: discord.Interaction,
                                select: app_commands.Choice[str],
                                clan_emblem: Optional[discord.Attachment]):
        """
        Create or edit a billboard ad.
        """
        view = BillboardView(interaction, ad_manager=self.ad_manager)

        if select.value == 'create':
            await view.load()

            # Build the embed.
            embed = Embed(
                title="_Shinobi of the Lotus#141_",
                description='\u200B',
                color=Color.red()
            )
            embed.add_field(
                name='Invite Requirements',
                value='\u200B',
                inline=False
            )
            embed.add_field(
                name="_Select invite status from the dropdown below._",
                value="\u200B",
                inline=True
            )
            embed.add_field(name="\u200B", value='_This is a sample._')
            await interaction.response.send_message(
                content='Your ad will be previewed here.',
                embed=embed,
                view=view,
                ephemeral=True
            )
        elif select.value == 'edit':
            # self.ad_manager.loads()
            member = interaction.user.id
            await self.ad_manager.load_ads()
            try:
                await self.ad_manager.read(str(interaction.user.id))
            except IDNotFoundException:
                await interaction.response.send_message(
                    content="It looks like you don't have an ad in the " \
                        "alliance-billboard channel. Please use " \
                        "\"/billboard Create Ad\" to create an ad.",
                    ephemeral=True
                )
                return

            title = await self.ad_manager.read(
                member, key=ClanAdKey.NAME)
            description = await self.ad_manager.read(
                member, key=ClanAdKey.DESCRIPTION)
            requirements = await self.ad_manager.read(
                member, key=ClanAdKey.REQUIREMENTS)
            clan_emblem_url = await self.ad_manager.read(
                member, key=ClanAdKey.CLAN_EMBLEM_URL)
            status_code = await self.ad_manager.read(
                member, key=ClanAdKey.INVITE_STATUS)
            invite_status = clan_ad.get(
                f"CLAN_AD_{status_code}")

            # Change the colour depending on the invite status.
            color = Color.green() if await self.ad_manager.read(
                member, key=ClanAdKey.INVITE_STATUS) == '0x0' else \
                Color.red()

            # Build the embed.
            embed = Embed(
                title=title, description=description, color=color
            )
            embed.add_field(
                name='Invite Requirements', value=requirements, inline=False
            )
            embed.add_field(
                name=invite_status, value="\u200B", inline=True
            )
            await interaction.response.send_message(
                content="Here is the ad preview. Select " \
                    "\"Post Ad\" when you're ready.",
                    embed=embed,
                    view=view,
                    ephemeral=True
            )

            guild = interaction.guild
            billboard_channel = guild.get_channel( #type: ignore
                settings['CHANNEL_ID']['ALLIANCE_BILLBOARD'])

    @app_commands.command(
            name='emblem-upload',
            description='Uploads a clan emblem to a billboard ad. ' \
            '128x128px, .png/.jpg recommended.')
    @app_commands.checks.has_any_role(
        settings['ROLE_ID']['WARLORD'])
    async def billboard_upload(self,
                               interaction: discord.Interaction,
                               attachment: Optional[discord.Attachment]):
        """Upload a clan emblem for the billboard ad."""
        # Due to a Discord limitation, we can't simply click on the
        # "Upload Clan Emblem" button and attach an image.
        # To workaround this, we need to create this command. If the member
        # doesn't have a clan ad being previewed or completed, then Seren
        # will say you need to do that first.

        # If the media type isn't a .jpg or .png, cancel the operation.
        # if attachment.content_type is not 'image/jpeg' or \
        #     attachment.content_type is not 'image/png':
        #     await interaction.response.send_message(
        #         content="This isn't a supported image format. Please " \
        #         "upload a .jpg or .png file of your clan emblem.",
        #         ephemeral=True
        #     )
        #     return

        # Checks if there's an ad made by the Alliance Warlord.

        # Checks if there's an ad being previewed.

        # If the above are not true, post an ephemeral message, stating they
        # need to at least have an ad previewed first.
