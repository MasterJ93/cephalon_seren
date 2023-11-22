"""
Manages the clan ads temporarily when using the "/billboard Create Ad"
Slash Command.
"""

from enum import Enum
from database.clan_ad_db import clan_ads


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

class IDAlreadyExistsException(Exception):
    """
    A custom exception for handling cases where a clan ID already exists.
    """


class IDNotFoundException(Exception):
    """
    A custom exception for handling cases where a clan ID hasn't been found.
    """


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
        user_id = self._get_user_id(user_id)

        # If the user ID already exists, then an error is thrown.
        if user_id in clan_ads:
            raise IDAlreadyExistsException(f"ID {user_id} already exists.")

        clan_ads[user_id] = {
            'NAME': name,
            'DESCRIPTION': description,
            'REQUIREMENTS': requirements,
            'CLAN_EMBLEM_URL': clan_emblem_url,
            'INVITE_STATUS': invite_status,
            'MESSAGE_ID': message_id
        }

        return clan_ads[user_id]


    def find(self, user_id: int):
        """
        Finds the dictionary entry for the clan ad.
        """
        if user_id not in clan_ads:
            raise IDNotFoundException(f"Couldn't find ID {user_id}.")

        return clan_ads[user_id]

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
