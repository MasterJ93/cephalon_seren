"""
Manages the clan ads temporarily when using the "/billboard Create Ad"
Slash Command.
"""

import asyncio
import json
import os
from enum import Enum
from typing import Optional

import aiofiles

from utils.exceptions import (
    IDAlreadyExistsException,
    IDNotFoundException
)


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
    BANNED_MEMBERS = 'BANNED_MEMBERS'


class ClanAdManager():
    """
    Accesses the clan ads within the 'clan_ad_db.py' file.
    """

    def __init__(self):
        self.lock = asyncio.Lock()

        # Gets the directory where `clan_ad_manager.py` is located
        base_dir = os.path.dirname(os.path.dirname(__file__))
        # Constructs the path to the JSON file relative to the base directory
        self.json_file = os.path.join(
            base_dir, 'database', 'clan_ads_db.json'
        )
        # self.json_file = '../database/clan_ads_db.json'
        self.clan_ads = {}

    async def load_ads(self):
        """
        Loads the JSON into memory.
        """
        print('Loading the data.')
        self.clan_ads = await self._load_data()

    async def _load_data(self):
        try:
            print('Trying this method...')
            async with self.lock:
                print('Safety lock on.')
                async with aiofiles.open(
                        self.json_file, 'r', encoding='utf-8') as file:
                    data = await file.read()
                    print(f'data: {data}')
                    return json.loads(data).get("clan_ads", {})
        except FileNotFoundError:
            print("Can't find the data. Returning an empty dictionary.")
            return {}

    async def _save_data(self):
        async with self.lock:
            async with aiofiles.open(
                    self.json_file, 'w', encoding='utf-8') as file:
                data = {"clan_ads": self.clan_ads}
                await file.write(json.dumps(data, indent=4))

    async def create(self, user_id, name="", description="", requirements="",
                     clan_emblem_url="", invite_status="", message_id=0,
                     banned_members=None):
        """
        Creates a dictionary entry for the clan ad.
        """
        # Cast user_id to a str.
        user_id = str(user_id)

        async with self.lock:
            if user_id in self.clan_ads:
                raise IDAlreadyExistsException(
                    f"ID ({user_id}) already exists.")

            if banned_members is None:
                banned_members = []

            self.clan_ads[user_id] = {
                'NAME': name,
                'DESCRIPTION': description,
                'REQUIREMENTS': requirements,
                'CLAN_EMBLEM_URL': clan_emblem_url,
                'INVITE_STATUS': invite_status,
                'MESSAGE_ID': message_id,
                'BANNED_USERS': banned_members
            }

        await self._save_data()
        return self.clan_ads[user_id]

    async def read(self, user_id, key: Optional[ClanAdKey] = None):
        """
        Reads the dictionary for the clan ad. If key is provided,
        returns the specific value. Otherwise, returns the entire
        clan ad entry.
        """
        # Cast user_id to a str.
        user_id = str(user_id)

        async with self.lock:
            print('Locking .read()')
            print(f'self.clan_ads: {self.clan_ads}')

            if user_id not in self.clan_ads:
                print("Couldn't find ID in .read()")
                raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

            if key is not None:
                return self.clan_ads[user_id].get(key.value)
            else:
                return self.clan_ads[user_id]

    async def update(self, user_id, **kwargs):
        """
        Updates a value for a key in the clan ad's dictionary.
        """
        # Cast user_id to a str.
        user_id = str(user_id)

        async with self.lock:
            print(f"In update(), the clan_ads dictionary are of the following:\n{self.clan_ads}")
            if user_id not in self.clan_ads:
                print('Raising error in update().')
                raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

            valid_keys = {key.value for key in ClanAdKey}
            print(f"value_keys: {valid_keys}")
            for key, value in kwargs.items():
                print(f"Key-Value pair: ({key}), ({value})")
                if key.upper() == 'BANNED_MEMBERS':
                    self.clan_ads[user_id][key.upper()] = value
                elif key.upper() in valid_keys and value is not None:
                    self.clan_ads[user_id][key.upper()] = value
                elif key.upper() not in valid_keys:
                    raise ValueError(f"Key ({key}) is invalid.")

        await self._save_data()

    async def delete(self, user_id):
        """
        Deletes the entire clan ad's dictionary.
        """
        # Cast user_id to a str.
        user_id = str(user_id)

        async with self.lock:
            if user_id not in self.clan_ads:
                raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

            del self.clan_ads[user_id]
        await self._save_data()

    async def is_user_banned(self, user_id, banned_member_id):
        """
        Checks if a member is in the BANNED_MEMBERS list of a
        specific clan ad.
        """
        async with self.lock:
            clan_ad = self.clan_ads.get(str(user_id))
            if clan_ad and banned_member_id in clan_ad.get(
                'BANNED_MEMBERS', []
                ):
                return True

        return False

    async def add_banned_user(self, user_id, banned_member_id):
        """
        Adds a user ID to the BANNED_USERS list for a specific clan ad.
        """
        async with self.lock:
            if user_id not in self.clan_ads:
                raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

            if banned_member_id not in self.clan_ads[user_id].get(
                'BANNED_USERS', []
                ):
                self.clan_ads[user_id]['BANNED_USERS'].append(
                    banned_member_id
                    )
                await self._save_data()

    async def remove_banned_user(self, user_id, banned_member_id):
        """
        Remove a user ID from the BANNED_MEMBERS list for a
        specific clan ad.
        """
        async with self.lock:
            if user_id not in self.clan_ads:
                raise IDNotFoundException(f"Couldn't find ID ({user_id}).")

            if banned_member_id in self.clan_ads[user_id].get(
                'BANNED_USERS', []
                ):
                self.clan_ads[user_id]['BANNED_USERS'].remove(
                    banned_member_id
                    )
                await self._save_data()
