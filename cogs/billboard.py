"""
A list of commands related to managing ads in the
alliance-billboard channel.
"""

import discord
from discord import Embed, app_commands
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
    @app_commands.choices(choices=[
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
                                choices: app_commands.Choice[str]):
        """
        Create or edit a billboard ad.
        """
        guild = interaction.guild
        billboard_channel = guild.get_channel( #type: ignore
                settings['CHANNEL_ID']['ALLIANCE_BILLBOARD'])

        if choices.value == 'create':
            # await billboard_channel.send( #type: ignore
            #     content='',
            #     embed=Embed()
            # )
            view = BillboardView(interaction)
            # await interaction.response.send_modal(BillboardClanModal(
            #     interaction.guild, interaction.user))
            await interaction.response.send_message(
                content='Your ad will be previewed here.',
                view=view
            )
        elif choices.value == 'edit':
            # message = await billboard_channel.fetch_message()
            pass
