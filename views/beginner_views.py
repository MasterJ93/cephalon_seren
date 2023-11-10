"""
Contains views related to members that just came into the server.
"""
import discord
from discord.ext import commands

class BeginnerView(discord.ui.View):
    """Contains a view for the beginner message."""
    def __init__(self):
        super().__init__()
