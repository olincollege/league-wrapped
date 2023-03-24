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
