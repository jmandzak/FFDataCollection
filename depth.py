import typing

import pandas as pd
import requests
from bs4 import BeautifulSoup
from FootballNameMatcher import match_name

URL = "https://fftoolbox.fulltimefantasy.com/football/depth-charts.cfm"


def _get_depth_and_name(
    player: str,
) -> typing.Tuple[typing.Optional[str], typing.Optional[str]]:
    # The format is QB1 Name, QB2 Name, etc. We want to split the number and name
    depth, name = player.split(" ", 1)
    if depth[:-1] not in ["QB", "RB", "WR", "TE", "PK"]:
        return None, None
    depth = depth[-1]
    name = match_name(name, force_last_name_match=True)
    return depth, name


def _remove_unmatched_players(
    names: typing.List[str], depths: typing.List[str]
) -> None:
    indices_to_remove = []
    for i, name in enumerate(names):
        if name is None:
            indices_to_remove.append(i)
    for i in reversed(indices_to_remove):
        names.pop(i)
        depths.pop(i)


def main() -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    page = requests.get(URL, headers=headers, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    # Each team is in a div with class "team"
    teams = soup.find_all("div", class_="team")
    # Each team div contains a ul with li elements for each player. Get all li elements
    players = [team.find_all("li") for team in teams]
    # Collapse the list of lists into a single list
    players = [player for team in players for player in team]
    # Extract the player name from the li element
    players = [player.text.strip() for player in players]
    names = []
    depths = []
    for player in players:
        depth, name = _get_depth_and_name(player)
        if depth is None or name is None:
            continue
        names.append(name)
        depths.append(depth)
    _remove_unmatched_players(names, depths)
    df = pd.DataFrame(data=zip(names, depths), columns=["PLAYER NAME", "DEPTH"])
    df.to_csv("stats24/all_depth_chart.csv", index=False)


if __name__ == "__main__":
    main()
