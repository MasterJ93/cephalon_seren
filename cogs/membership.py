"""
membership.py: A discord.py cog for Cephalon Seren that manages server membership
features, such as assigning roles to new members and sending them
a message to inquire about their interest in joining the clan.
"""
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from config import settings

