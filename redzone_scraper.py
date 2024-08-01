import typing

import bs4
import pandas
import requests
from FootballNameMatcher.match import match_name

from constants import REDZONE_RECEIVING_COLUMNS, REDZONE_RUSHING_COLUMNS, REDZONE_URLs


def scrape_receiving_redzone() -> (
    typing.List[typing.List[typing.Union[str, int, float]]]
):
    response = requests.get(REDZONE_URLs["receiving"])
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # get the table with id fantasy_rz
    table = soup.find("table", {"id": "fantasy_rz"})
    players = []
    for row in table.find_all("tr"):  # type: ignore
        player = []
        name = match_name(row.find("th").text, min_score=50)
        cells = row.find_all("td")
        if len(cells) == 0:
            continue

        # columns are Tm	Tgt	Rec	Ctch%	Yds	TD	%Tgt	Tgt	Rec	Ctch%	Yds	TD	%Tgt	Link
        # We want Tgt, %Tgt, Tgt, %Tgt
        player.append(name)
        player.append(cells[1].text)
        player.append(cells[6].text.strip()[:-1])
        player.append(cells[7].text)
        player.append(cells[12].text.strip()[:-1])
        for val in player:
            if val == "":
                val = 0
        players.append(player)

    return players


def scrape_rushing_redzone() -> typing.List[typing.List[typing.Union[str, int, float]]]:
    response = requests.get(REDZONE_URLs["rushing"])
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # get the table with id fantasy_rz
    table = soup.find("table", {"id": "fantasy_rz"})
    players = []
    for row in table.find_all("tr"):  # type: ignore
        player = []
        name = match_name(row.find("th").text, min_score=50)
        if name is None:
            continue
        cells = row.find_all("td")
        if len(cells) == 0:
            continue

        # columns are Tm	Att	Yds	TD	%Rush	Att	Yds	TD	%Rush	Att	Yds	TD	%Rush
        # We want Att, %Rush, Att, %Rush, Att, %Rush
        player.append(name)
        player.append(cells[1].text)
        player.append(cells[4].text.strip()[:-1])
        player.append(cells[5].text)
        player.append(cells[8].text.strip()[:-1])
        player.append(cells[9].text)
        player.append(cells[12].text.strip()[:-1])
        for i, val in enumerate(player):
            if val == "":
                player[i] = 0
        players.append(player)

    return players


def main() -> None:
    rushing = scrape_rushing_redzone()
    receiving = scrape_receiving_redzone()

    rushing_csv = "stats24/rushing_redzone.csv"
    receiving_csv = "stats24/receiving_redzone.csv"

    pandas.DataFrame(rushing, columns=REDZONE_RUSHING_COLUMNS).to_csv(
        rushing_csv, index=False
    )
    pandas.DataFrame(receiving, columns=REDZONE_RECEIVING_COLUMNS).to_csv(
        receiving_csv, index=False
    )


if __name__ == "__main__":
    main()
