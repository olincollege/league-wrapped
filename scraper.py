"""
Functions for scraping League of Legends game stats from the Riot API
"""

from riotwatcher import LolWatcher
import pandas as pd

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

    Returns:
        A DataFrame holding all player stats from all matches in matchlist
    """
    summoner = watcher.summoner.by_name(region, summoner_name)

    player_keys = watcher.match.by_id(region, matchlist[0])["info"]["participants"][
        0
    ].keys()
    player_stats = pd.DataFrame(index=matchlist, columns=player_keys)

    for match_id in matchlist:
        current_match = watcher.match.by_id(region, match_id)
        if (
            current_match["info"]["gameMode"] != "CLASSIC"
            or current_match["info"]["gameDuration"] < 240
        ):
            player_stats = player_stats.drop([match_id])
            continue

        target_player = next(
            (
                player
                for player in current_match["info"]["participants"]
                if player["puuid"] == summoner["puuid"]
            )
        )

        player_stats.loc[match_id] = target_player

        player_stats.to_csv(f"{summoner_name}.csv")

    return player_stats
