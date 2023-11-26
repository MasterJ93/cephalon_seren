"""Helper classes and methods."""
import asyncio
import io
import json
from urllib.parse import unquote, urlparse

import aiohttp

from utils.exceptions import RequestFailedException


class JSONRuleReader():
    """Reads rules in JSON for Cephalon Seren."""
    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file
        self.rules = self.read_json_file()

    def read_json_file(self):
        """Reads the JSON file."""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print('File not found.')
            return {"rules": []}
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            return {"rules": []}
        except IOError as e:
            print(f"IO error occurred: {e}")
            return {"rules": []}

    def get_selected_rules(self, rule_numbers):
        """Puts the selected rules into a list."""
        selected_rules = []
        for rule in rule_numbers:
            # Extract the rule number from the string and convert it
            # to an index. The rule number is assumed to be before the
            # first '.' in the string. Subtract 1 to convert from 1-based
            # to 0-based indexing.

            # Convert the first part to integer and adjust for zero-based
            # indexing.
            rule_index = int(rule.split('.')[0]) - 1

            # Check if the calculated index is within the range of
            # available rules. This ensures we don't try to access an index
            # that doesn't exist in the rules list
            if 0 <= rule_index < len(self.rules['rules']):
                # If the index is valid, append the corresponding rule to
                # the selected_rules list
                selected_rules.append(self.rules['rules'][rule_index])

        # Convert all of this into a string.
        rule_string = ''

        for rule in selected_rules:
            rule_string += f'> {rule}\n'

        return rule_string

class ImgDownloader():
    """Downloads images from the server."""

    async def download(self, url):
        """Downloads the image from the URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise RequestFailedException()
                return io.BytesIO(await resp.read())
