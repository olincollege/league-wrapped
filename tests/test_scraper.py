"""
Check that scraper functions are setup properly
"""

import os
import sys
from requests.exceptions import HTTPError

sys.path.append("./modules")

# pylint: disable=import-error, wrong-import-position
from scraper import create_watcher


def test_key_file_exists():
    """
    Test `key.txt` exists
    """
    assert os.path.exists("key.txt")


def test_key_validity():
    """
    Test api key is valid
    """
    try:
        create_watcher().champion.rotations("na1")
    except HTTPError:
        assert False
