"""
Functions for analyzing League of Legends game stats
"""


def most_deaths(player_data):
    """
    Finds the most number of deaths in one game and the champion that was
    being played

    Args:
        player_data: A DataFrame holding a player's stats from various matches

    Returns:
        A tuple holding an integer, representing the number of deaths, and
        a string, representing the champion name
    """
    max_deaths = player_data["deaths"].max()
    champ_name = player_data[player_data["deaths"] == max_deaths]["championName"][0]
    return (max_deaths, champ_name)


def least_cs(player_data):
    """
    Finds the least cs (creep score) per minute in one game and the champion
    that was being played

    Args:
        player_data: A DataFrame holding a player's stats from various matches

    Returns:
        A tuple holding an float, represetning the cs/m, and a string,
        representing the champion name
    """
    player_data["cs/m"] = (
        player_data["neutralMinionsKilled"] + player_data["totalMinionsKilled"]
    ) / (player_data["timePlayed"] / 60)
    min_cs = player_data[
        (player_data["individualPosition"] != "UTILITY")
        & (player_data["role"] != "SUPPORT")
        & (player_data["teamPosition"] != "UTILITY")
    ]["cs/m"].min()
    champ_name = player_data[player_data["cs/m"] == min_cs]["championName"][0]
    return (min_cs, champ_name)


def worst_winrate(player_data):
    """
    Finds the five champions, that have more than five games played,
    with the worst winrates

    Args:
        player_data: A DataFrame holding a player's stats from various matches

    Returns:
        A list of dictionaries representing the five champions with the worst
        winrates. Each dictionary holds the champion's name, winrate, and
        number of games played
    """
    champs_played = player_data["championName"].unique()

    champ_wrs = []

    for champ in champs_played:
        champ_games = player_data[player_data["championName"] == champ]["win"]
        games_played = len(champ_games)
        if games_played < 5:
            continue
        winrate = sum(champ_games) / games_played

        champ_wrs.append(
            {
                "champ": champ,
                "winrate": winrate,
                "games_played": games_played,
            }
        )

    return sorted(champ_wrs, key=lambda champ_dict: champ_dict["wr"])[:5]
