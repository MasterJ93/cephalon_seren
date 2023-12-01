"""
Helper classes and methods.
"""
import io
import json
from urllib.parse import unquote, urlparse

import aiohttp

from utils.exceptions import RequestFailedException


class JSONRuleReader():
    """
    Reads rules in JSON for Cephalon Seren.
    """
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
        """
        Puts the selected rules into a list.
        """
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

class URLParser():
    """
    Helper class that parses URLs to use in grabbing the file name.
    """
    def get_file_name(self, url, only_protocol=False):
        """Parses a URL to get the resulting file name.

        Args:
            Args:
            url (str): The URL to parse.
            only_protocol (bool): If True, only removes the
            protocol from the URL.
        """
        # Parse the URL
        parsed_url = urlparse(url)

        # Only the protocol if 'only_protocol' is set to True.
        if only_protocol:
            return (
                parsed_url.netloc + parsed_url.path +
                parsed_url.query + parsed_url.fragment
            )

        # Extract the file name from the path
        path = parsed_url.path
        file_name = unquote(path.split('/')[-1])
        return file_name

class ImgDownloader():
    """
    Downloads images from the server.
    """

    async def download(self, url):
        """
        Downloads the image from the URL.

        Args:
            url (str): The URL used to download the image.
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        raise RequestFailedException()
                    return io.BytesIO(await resp.read())
        except aiohttp.client.InvalidURL as exc:
            raise RequestFailedException(f"Invalid URL: {url}") from exc
