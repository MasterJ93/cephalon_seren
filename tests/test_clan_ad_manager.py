"""
This test suite covers the functionality of the ClanAdManager class.
"""
# pylint: disable=unused-argument
from unittest.mock import AsyncMock, patch

import pytest

from utils.clan_ad_manager import ClanAdManager


@pytest.fixture
def mock_aiofile():
    mock = AsyncMock()
    mock.__aenter__.return_value.read = AsyncMock(return_value='{"clan_ads": {"226514864258940930": {"NAME": "", "DESCRIPTION": "", "REQUIREMENTS": "", "CLAN_EMBLEM_URL": "https://media.discordapp.net/ephemeral-attachments/1172080798099324949/1178619574288121886/Delilah.png", "INVITE_STATUS": "", "MESSAGE_ID": 0}}}')
    with patch('aiofiles.open', return_value=mock):
        yield mock


@pytest.mark.asyncio
async def test_load_ads_success(mock_aiofile):
    manager = ClanAdManager()
    await manager.load_ads()

    assert manager.clan_ads == {
        "226514864258940930": {
            "NAME": "",
            "DESCRIPTION": "",
            "REQUIREMENTS": "",
            "CLAN_EMBLEM_URL": "https://media.discordapp.net/ephemeral-attachments/1172080798099324949/1178619574288121886/Delilah.png",
            "INVITE_STATUS": "",
            "MESSAGE_ID": 0
        }
    }



@pytest.mark.asyncio
async def test_load_ads_file_not_found():
    # Simulate FileNotFoundError
    answer = 1 + 1
    assert answer == 2
    with patch('aiofiles.open', side_effect=FileNotFoundError):
        manager = ClanAdManager()
        await manager.load_ads()

        # Expect the clan_ads to be an empty dictionary after FileNotFoundError
        assert manager.clan_ads == {}


# import asyncio
# import json
# from unittest.mock import AsyncMock, MagicMock, patch

# import pytest

# from utils.clan_ad_manager import ClanAdKey, ClanAdManager

## A fixture for creating a mock object
# @pytest.fixture
# def mock_api_client():
#     return MagicMock()