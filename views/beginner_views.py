"""
Contains views related to members that just came into the server.
"""
import discord
from utils.messages import beginner
from config import settings

class BeginnerViewDropdown(discord.ui.Select):
    """Contains a dropdown for the beginner view."""
    def __init__(self):
        options = [
            discord.SelectOption(label=beginner['DROPDOWN_OPTION_1']),
            discord.SelectOption(label=beginner['DROPDOWN_OPTION_2']),
            discord.SelectOption(label=beginner['DROPDOWN_OPTION_3'])
        ]
        super().__init__(placeholder='Choose an option...', options=options)

    async def callback(self, interaction: discord.Interaction):
        seren_message = await interaction.original_response()
        mentioned_member = seren_message.raw_mentions[0]
        response = interaction.response

        # Checks if the member who interacted with the original message is
        # the one Seren mentioned.
        if interaction.user.id is not mentioned_member:
            return

        if self.values[0]:
            await response.send_message(
                content=beginner['OPTION_1_RESPONSE'],
                ephemeral=True,
                delete_after=60.0
            )
        elif self.values[1]:
            await response.send_message(
                content=beginner['OPTION_2_RESPONSE'].format(
                    billboards=settings['CHANNEL_ID']['ALLIANCE_BILLBOARD']),
                ephemeral=True,
                delete_after=60.0
            )
        elif self.values[2]:
            await response.send_message(
                content=beginner['OPTION_3_RESPONSE'],
                ephemeral=True,
                delete_after=60.0
            )


class BeginnerView(discord.ui.View):
    """Contains a view for the beginner message."""
    def __init__(self):
        super().__init__()

        self.add_item(BeginnerViewDropdown())
