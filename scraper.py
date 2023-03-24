"""
Functions for scraping League of Legends game stats from the Riot API
"""

from riotwatcher import LolWatcher
from collections import defaultdict
import pandas as pd
from time import time

YEAR_SECONDS = 31536000
S12_START = 1641531600  # 1/07/2022, 00:00:00
S12_END = 1668488399  # 11/14/2022, 23:59:59


def create_watcher(filepath):
    """
    Creates a LolWatcher object using an API key from a file

    Args:
        filepath: A string representing the filepath to .txt file with the key
            as the first and only line

    Returns:
        A LolWatcher object using the given API key
    """
    with open(filepath, "r", encoding="UTF=8") as file:
        api_key = file.readline()
    return LolWatcher(api_key)


def get_season_matchlist(watcher, summoner_name, region):
    """
    Create a list of match ids for all matches played by a summoner in
    Season 12. The match ids are ordered from most recent to least recent.

    Args:
        watcher: A LolWatcher object holding an API key
        summoner_name: A string representing the name of the summoner who's
            matches will be found
        region: A string representing the region of the summoner
            regions can be found here: https://developer.riotgames.com/docs/lol
            under "platform routing values"

    Returns:
        A list of strings representing the match ids
    """
    summoner = watcher.summoner.by_name(region, summoner_name)

    matchlist = []
    start_idx = 0

    while True:
        new_matchlist = watcher.match.matchlist_by_puuid(
            region=region,
            puuid=summoner["puuid"],
            start=start_idx,
            count=100,
            start_time=S12_START,
            end_time=S12_END,
        )
        matchlist += new_matchlist

        if len(new_matchlist) != 100:
            break

        start_idx += 100
    return matchlist


def get_matchlist(watcher, summoner_name, region, match_count):
    """
    Create a list of match ids of matches played by a summoner in the past
    year. The number of match ids is specified by `match_count`. The match ids
    are ordered from most recent to least recent.

    Args:
        watcher: A LolWatcher object holding an API key
        summoner_name: A string representing the name of the summoner who's
            matches will be found
        region: A string representing the region of the summoner
            regions can be found here: https://developer.riotgames.com/docs/lol
            under "platform routing values"
        match_count: An integer representing the number of match ids in the
            list

    Returns:
        A list of strings representing the match ids
    """
    summoner = watcher.summoner.by_name(region, summoner_name)
    return watcher.match.matchlist_by_puuid(
        region=region,
        puuid=summoner["puuid"],
        count=match_count,
        start_time=round(time() - YEAR_SECONDS),
        end_time=round(time()),
    )


def get_data_from_matchlist(watcher, summoner_name, matchlist, region):
    """
    Scrapes and concatenates data from matches into a Pandas DataFrame

    Args:
        watcher: A LolWatcher object holding an API key
        summoner_name: A string representing the name of the summoner who's
            data will be collected
        matchlist: A list of strings representing match ids
        region: A string representing the region of the summoner
            regions can be found here: https://developer.riotgames.com/docs/lol
            under "platform routing values"
    """
    player_stats = defaultdict(list)
    for match in matchlist:
        current_match = watcher.match.by_id(region=region, match_id=match)
        if (
            current_match["info"]["gameMode"] != "CLASSIC"
            or current_match["info"]["gameDuration"] < 240
        ):
            continue

        target_player = next(
            (
                player
                for player in current_match["info"]["participants"]
                if player["summonerName"] == summoner_name
            )
        )

        for stat in target_player:
            player_stats[stat].append(target_player[stat])

    return pd.DataFrame(player_stats)
