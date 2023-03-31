"""
Check that scraper functions are setup properly
"""

import os


def test_key_file_exists():
    """
    Test `key.txt` exists
    """
    assert os.path.exists("key.txt")
