"""
Check the correctness of analysis functions
"""

import sys
import pandas as pd

sys.path.append("./modules")

# pylint: disable=import-error, wrong-import-position
from analysis import (
    least_cs,
    most_deaths,
    worst_kda,
    worst_vs,
    worst_winrate,
)

IAN_DATA = pd.read_csv("./data/Among Us Jimin.csv", index_col=0)


def test_least_cs():
    """
    Test least_cs function's correctness
    """
    assert least_cs(IAN_DATA) == (2.9377880184331797, "Janna")


def test_most_deaths():
    """
    Test least_cs function's correctness
    """
    assert most_deaths(IAN_DATA) == (13, "Ashe")


def test_worst_kda():
    """
    Test least_cs function's correctness
    """
    assert worst_kda(IAN_DATA) == [
        {"champ": "Olaf", "kda": 0.16666666666666666, "games_played": 1},
        {"champ": "Nilah", "kda": 0.7142857142857143, "games_played": 1},
        {"champ": "Garen", "kda": 0.8181818181818182, "games_played": 2},
        {"champ": "Nasus", "kda": 1.0, "games_played": 1},
        {"champ": "Viego", "kda": 1.125, "games_played": 1},
    ]


def test_worst_vs():
    """
    Test least_cs function's correctness
    """
    assert worst_vs(IAN_DATA) == (0.055299539170506916, "Karma")


def test_worst_winrate():
    """
    Test least_cs function's correctness
    """
    assert worst_winrate(IAN_DATA) == [
        {"champ": "Zilean", "winrate": 0.0, "games_played": 7},
        {"champ": "Evelynn", "winrate": 0.16666666666666666, "games_played": 6},
        {"champ": "Seraphine", "winrate": 0.2857142857142857, "games_played": 7},
        {"champ": "Kaisa", "winrate": 0.3, "games_played": 10},
        {"champ": "Quinn", "winrate": 0.3333333333333333, "games_played": 6},
    ]
