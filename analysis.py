"""
Functions for analyzing League of Legends game stats
"""


def most_deaths(player_data):
    """
    Finds the most number of deaths in one game and the champion that was
    being played

    Args:
        player_data: A DataFrame holding a players stats from various matches

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
        player_data: A DataFrame holding a players stats from various matches

    Returns:
        A tuple holding an float, represetning the cs/m, and a string,
        representing the champion name
    """
    player_data["cs/m"] = (
        player_data["neutralMinionsKilled"] + player_data["totalMinionsKilled"]
    ) / (player_data["timePlayed"] / 60)
    min_cs = player_data[player_data["individualPosition"] != "UTILITY"]["cs/m"].min()
    champ_name = player_data[player_data["cs/m"] == min_cs]["championName"][0]
    return (min_cs, champ_name)
