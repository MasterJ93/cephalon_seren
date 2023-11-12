"""
Contains views related to members that just came into the server.
"""
import discord
from utils.messages import beginner

class OnboardView(discord.ui.View):
    """Contains a view for first-time members."""
    def __init__(self, user_id: int, alliance_channel: discord.TextChannel):
        super().__init__()
        self.user_id = user_id
        self.alliance_channel = alliance_channel
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
        """When the first option is selected."""
        label = button.label
        print(f"\"{label}\" selected.")

        response = interaction.response
        response_message = beginner['OPTION_1_RESPONSE']

        await response.send_message(
            content=response_message,
            ephemeral=True,
            delete_after=60.0
        )

    @discord.ui.button(
        label=beginner['DROPDOWN_OPTION_2'],
        style=discord.ButtonStyle.green
    )
    async def selection_2(self,
                          interaction: discord.Interaction,
                          button: discord.ui.Button):
        """When the second option is selected."""
        label = button.label
        print(f"\"{label}\" selected.")

        response = interaction.response
        response_message = beginner['OPTION_2_RESPONSE'].format(
                    billboards=self.alliance_channel.mention
        )

        await response.send_message(
            content=response_message,
            ephemeral=True,
            delete_after=60.0
        )

    @discord.ui.button(
        label=beginner['DROPDOWN_OPTION_3'],
        style=discord.ButtonStyle.green
    )
    async def selection_3(self,
                          interaction: discord.Interaction,
                          button: discord.ui.Button):
        """When the first option is selected."""
        label = button.label
        print(f"\"{label}\" selected.")

        response = interaction.response
        response_message = beginner['OPTION_3_RESPONSE']

        await response.send_message(
            content=response_message,
            ephemeral=True,
            delete_after=60.0
        )
