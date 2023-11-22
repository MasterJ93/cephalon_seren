"""
Manages the clan ads temporarily when using the "/billboard Create Ad"
Slash Command.
"""

from enum import Enum


class ClanAdKey(Enum):
    """
    Enum for defining valid keys in clan ad entries.
    """
    NAME = 'NAME'
    DESCRIPTION = 'DESCRIPTION'
    REQUIREMENTS = 'REQUIREMENTS'
    CLAN_EMBLEM_URL = 'CLAN_EMBLEM_URL'
    INVITE_STATUS = 'INVITE_STATUS'
    MESSAGE_ID = 'MESSAGE_ID'


class ClanAdManager():
    """Accesses the clan ads within the \"clan_ad_db.py\" file."""
    def __init__(self, user_id):
        self.user_id = user_id

    def _get_user_id(self, user_id=None):
        """
        Determines whether to use `id` or `self.user_id`, depending on if `user_id` is
        not `None`.
        """
        return user_id if user_id is not None else self.user_id

    def create(self, user_id=None, name="", description="", requirements="",
               clan_emblem_url="", invite_status="", message_id=0):
        """
        Creates a dictionary entry for the clan ad.
        """

    def find(self, user_id: int):
        """
        Finds the dictionary entry for the clan ad.
        """

    def read(self, key=None, user_id=None):
        """
        Reads the dictionary for the clan ad.
        """

    def update(self, user_id=None, **kwargs):
        """
        Updates a value for a key in the clan ad's dictionary.
        """

    def delete(self, user_id=None):
        """
        Deletes the entire clan ad's dictionary.
        """
