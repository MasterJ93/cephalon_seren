"""
Manages the clan ads temporarily when using the "/billboard Create Ad"
Slash Command.
"""

import json
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
        self.json_file = '../database/clan_ads_db.json'
        self.clan_ads = self._load_data()

    def _load_data(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("clan_ads", {})
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.json_file, 'w', encoding='utf-8') as file:
            data = {"clan_ads": self.clan_ads}
            json.dump(data, file, indent=4)

    def _get_user_id(self, user_id=None):
        print(f'user_id is {user_id}. self.user_id is {self.user_id}.')
        return user_id if user_id is not None else self.user_id

    def create(self, user_id=None, name="", description="", requirements="",
               clan_emblem_url="", invite_status="", message_id=0):
        """
        Creates a dictionary entry for the clan ad.
        """
        user_id = self._get_user_id(user_id)

        if user_id in self.clan_ads:
            raise IDAlreadyExistsException(f"ID ({user_id}) already exists.")

        self.clan_ads[user_id] = {
            'NAME': name,
            'DESCRIPTION': description,
            'REQUIREMENTS': requirements,
            'CLAN_EMBLEM_URL': clan_emblem_url,
            'INVITE_STATUS': invite_status,
            'MESSAGE_ID': message_id
        }
        print(f'{user_id} has been created:\n{self.clan_ads[user_id]}')
        self._save_data()
        return self.clan_ads[user_id]


    def find(self, user_id: int):
        """
        Finds the dictionary entry for the clan ad.
        """
        if user_id not in self.clan_ads:
            raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

        return self.clan_ads[user_id]

    def read(self, key: ClanAdKey, user_id=None):
        """
        Reads the dictionary for the clan ad.
        """
        user_id = self._get_user_id(user_id)

        if user_id not in self.clan_ads:
            raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

        return self.clan_ads[user_id].get(key.value)


    def update(self, user_id=None, **kwargs):
        """
        Updates a value for a key in the clan ad's dictionary.
        """
        user_id = self._get_user_id(user_id)

        if user_id not in self.clan_ads:
            raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

        valid_keys = {key.value for key in ClanAdKey}
        for key, value in kwargs.items():
            if key.upper() in valid_keys and value is not None:
                self.clan_ads[user_id][key.upper()] = value
            elif key.upper() not in valid_keys:
                raise ValueError(f"Key ({key}) is invalid.")

        self._save_data()

    def delete(self, user_id=None):
        """
        Deletes the entire clan ad's dictionary.
        """
        user_id = self._get_user_id(user_id)

        if user_id not in self.clan_ads:
            raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

        del self.clan_ads[user_id]
        self._save_data()
