"""
A list of commands related to managing ads in the
alliance-billboard channel.
"""

from typing import Optional

import discord
from discord import Color, Embed, app_commands
from discord.abc import MISSING
from discord.ext import commands

from config import settings
from utils.clan_ad_manager import (
    ClanAdKey,
    ClanAdManager
)
from utils.exceptions import InvalidFileType, IDNotFoundException
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
        clan_emblem='Upload a clan emblem to a billboard ad. '
            '128x128px, .png/.jpg recommended.'
        )
    @app_commands.choices(select=[
            app_commands.Choice(
                name="Create Ad", value="create"),
            # app_commands.Choice(
            #     name="Edit Ad", value="edit"),
            app_commands.Choice(
                name="Delete Ad", value="delete")
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
        # If the checks fail for whatever reason, stop running the
        # Slash Command.
        try:
            resolved_attachment = await self.clan_emblem_handler(
                interaction, clan_emblem
            )
        except InvalidFileType:
            return

        member = interaction.user.id
        view = BillboardView(
            interaction, ad_manager=self.ad_manager)
        await view.load()

        if select.value == 'create':
            await interaction.response.defer(ephemeral=True)
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
            if resolved_attachment is not None or resolved_attachment == '':
                embed.set_thumbnail(
                    url=f"attachment://{resolved_attachment.filename}"
                )
                print('resolved_attachment is not None.')
            else:
                print('resolved_attachment is None.')
                resolved_attachment=MISSING
            embed.add_field(name="\u200B", value='_This is a sample._')
            message = await interaction.followup.send(
                content='Your ad will be previewed here.',
                file=resolved_attachment, #type: ignore
                embed=embed,
                view=view,
                ephemeral=True
            )

            # Grab image URL for adding to the database (if it exists).
            message_embeds = message.embeds[0] #type: ignore
            file_url = (message_embeds.thumbnail.proxy_url #type: ignore
                        if message_embeds.thumbnail.proxy_url #type: ignore
                        else None)
            if file_url is None:
                return

            print(f"File URL: {file_url}")
            updates={}
            updates[ClanAdKey.CLAN_EMBLEM_URL.name] = file_url

            if updates:
                await self.ad_manager.update(member, **updates)

        elif select.value == 'edit':
            # self.ad_manager.loads()
            await self.ad_manager.load_ads()
            try:
                await self.ad_manager.read(member)
            except IDNotFoundException:
                await interaction.response.send_message(
                    content="It looks like you don't have an ad in the "
                        "alliance-billboard channel. Please use "
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
                content="Here is the ad preview. Select "
                    "\"Post Ad\" when you're ready.",
                    embed=embed,
                    view=view,
                    ephemeral=True
            )


        elif select.value == 'delete':
            # Check if there's a member ID. If not, send a message that
            # it doesn't exist and end the operation.
            member = interaction.user.id
            await self.ad_manager.load_ads()

            try:
                await interaction.response.defer(ephemeral=True)
                await self.ad_manager.delete(member)
            except IDNotFoundException:
                await interaction.response.defer(ephemeral=True)
                content =("This message doesn't seem to exist. But if "
                    "that's not true, let an admin know.")

                # If there's an image trying to be uploaded, state
                # this is useless.
                if resolved_attachment is not None:
                    content = (f"{content} I also see a file. Since "
                        "you're deleting an ad, this isn't needed.")

                await interaction.response.send_message(
                    content=content,
                    ephemeral=True
                )

    async def clan_emblem_handler(
            self,
            interaction: discord.Interaction,
            attachment: Optional[discord.Attachment]):
        """
        Handles the Clan Emblem being uploaded.
        """
        # This method is dedicated to handling image attachments for
        # the Slash Command. Discord's current limitations prevent
        # re-uploading an image directly for updates. To change the
        # clan emblem image, users must use the Slash Command again.

        # If there's no attachment, end this method.
        if attachment is None:
            return

        # If the media type isn't a .jpg or .png, cancel the operation.
        if (attachment.content_type != 'image/jpeg' #type: ignore
            and attachment.content_type != 'image/png'): #type: ignore
            await interaction.response.send_message(
                content=("This isn't a supported image format. Please "
                    "upload a .jpg or .png file of your clan emblem."),
                    ephemeral=True
            )
            raise InvalidFileType("Unsupported image format.")

        # If the image is less than 150x150 px, send an ephemeral message,
        # saying that it's smaller than the recommended size, and it may be
        # hard to see.
        # if attachment.width < 150 and attachment.height < 150: #type: ignore
        #     await interaction.response.send_message(
        #         content=()"Looks like this clan emblem is pretty small. Just "
        #         "know that your emblem may not look as good since it's "
        #         "this small."),
        #         ephemeral=True
        #     )

        return await attachment.to_file() #type: ignore
