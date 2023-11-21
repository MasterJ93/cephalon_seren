"""
A list of commands related to managing ads in the
alliance-billboard channel.
"""

import discord
from discord import Embed, Color, app_commands
from discord.ext import commands
from config import settings
from views.billboard_views import BillboardClanModal, BillboardView

class BillBoardCommands(commands.Cog):
    """
    BillboardCommands Cog for handling billboard ad management.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="billboard")
    @app_commands.describe(select='What would you like to do?')
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
                                # attachment: discord.Attachment,
                                select: app_commands.Choice[str]):
        """
        Create or edit a billboard ad.
        """
        guild = interaction.guild
        billboard_channel = guild.get_channel( #type: ignore
                settings['CHANNEL_ID']['ALLIANCE_BILLBOARD'])

        if select.value == 'create':
            # await billboard_channel.send( #type: ignore
            #     content='',
            #     embed=Embed()
            # )
            view = BillboardView(interaction)

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
            # await interaction.response.send_modal(BillboardClanModal(
            #     interaction.guild, interaction.user))
            await interaction.response.send_message(
                content='Your ad will be previewed here.',
                embed=embed,
                view=view,
                ephemeral=True
            )
        elif select.value == 'edit':
            # message = await billboard_channel.fetch_message()
            pass

    @app_commands.command(
            name='emblem-upload',
            description='Uploads a clan emblem to a billboard ad. ' \
            '128x128px, .png/.jpg recommended.')
    @app_commands.checks.has_any_role(
        settings['ROLE_ID']['WARLORD'])
    async def billboard_upload(self,
                               interaction: discord.Interaction,
                               attachment: discord.Attachment):
        """Upload a clan emblem for the billboard ad."""
        # Due to a Discord limitation, we can't simply click on the
        # "Upload Clan Emblem" button and attach an image.
        # To workaround this, we need to create this command. If the member
        # doesn't have a clan ad being previewed or completed, then Seren
        # will say you need to do that first.

        # Checks if there's an ad made by the Alliance Warlord.

        # Checks if there's an ad being previewed.

        # If the above are not true, post an ephemeral message, stating they
        # need to at least have an ad previewed first.
