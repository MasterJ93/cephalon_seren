"""
A cog that lists slash commands for admins only.
"""

import discord
from discord import app_commands
from discord.ext import commands
from config import settings
from views.admin_views import WarnView

class AdminCommands(commands.Cog):
    """
    AdminCommands Cog for handling admin-only commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
            name='warn',
            description='Warns a member when they violate a rule.'
            )
    @app_commands.describe(
        member='The member you want to send a warning to.')
    @app_commands.checks.has_role(settings['ROLE_ID']['ADMIN'])
    async def warn_member(self,
                          interaction: discord.Interaction,
                          member: discord.Member
                          ):
        """Warns a member when they violate a rule."""
        view = WarnView(interaction, interaction.guild, member) # type: ignore
        await interaction.response.send_message(view=view)
        await view.wait()

        if view.confirm is True:
            pass
        else:
            view.clear_items()
            await interaction.edit_original_response(
                content='I\'ve cancelled the action.',
                view=view)
