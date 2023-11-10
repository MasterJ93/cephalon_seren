"""
Contains views related to members that just came into the server.
"""
import discord
from discord.ext import commands

# from utils import messages
from utils.messages import beginner

class BeginnerView(discord.ui.View):
    """Contains a view for the beginner message."""
    def __init__(self):
        super().__init__()

class BeginnerViewDropdown(discord.ui.Select):
    """Contains a dropdown for the beginner view."""
    def __init__(self):
        options = [
            discord.SelectOption(label=beginner['DROPDOWN_OPTION_1']),
            discord.SelectOption(label=beginner['DROPDOWN_OPTION_2']),
            discord.SelectOption(label=beginner['DROPDOWN_OPTION_3'])
        ]
        super().__init__(placeholder='Choose an option...', options=options)


    