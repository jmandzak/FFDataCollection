import typing

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from FootballNameMatcher.match import match_name

from constants import BOOM_BUST_COLUMNS, BOOM_BUST_URLs


class BoomStartBust:
    def __init__(self) -> None:
        self._games = 0
        self._boom = 0
        self._start = 0
        self._bust = 0
        self._ppr_boom = 0
        self._ppr_start = 0
        self._ppr_bust = 0

    def set_std(self, boom, start, bust) -> None:
        self._boom = boom
        self._start = start
        self._bust = bust

    def set_ppr(self, boom, start, bust) -> None:
        self._ppr_boom = boom
        self._ppr_start = start
        self._ppr_bust = bust

    def set_games(self, games) -> None:
        self._games = games


def _build_boom_bust_data() -> typing.Dict[str, BoomStartBust]:
    data: typing.Dict[str, BoomStartBust] = {}
    for position, url in BOOM_BUST_URLs.items():
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", {"id": "boom-bust"})
        rows = table.find_all("tr")[1:]  # type: ignore

        for row in rows:
            name, games, boom, start, bust = _extract_data_from_row(row)
            if name is None:
                continue
            if name not in data:
                data[name] = BoomStartBust()
            data[name].set_games(games)
            if "ppr" in position:
                data[name].set_ppr(boom, start, bust)
            else:
                data[name].set_std(boom, start, bust)
            if position == "qb":
                data[name].set_ppr(boom, start, bust)

    return data


def _extract_data_from_row(
    row: bs4.element.Tag,
) -> typing.Tuple[typing.Optional[str], int, int, int, int]:
    cells = row.find_all("td")
    name = cells[1].text
    start = name.find("(")
    name = name[:start].strip()
    name = match_name(name, force_last_name_match=True)
    games = int(cells[2].text)
    boom = int(cells[3].text[:-1])
    start = int(cells[5].text[:-1])
    bust = int(cells[-2].text[:-1])
    return name, games, boom, start, bust


def _create_csv(data: typing.Dict[str, BoomStartBust]) -> None:
    # Create dataframe where the columns are PLAYER NAME,GAMES,BOOM,STARTER,BUST,PPR_BOOM,PPR_STARTER,PPR_BUST
    player_names = []
    games = []
    boom = []
    start = []
    bust = []
    ppr_boom = []
    ppr_start = []
    ppr_bust = []
    for name, stats in data.items():
        player_names.append(name)
        games.append(stats._games)
        boom.append(stats._boom)
        start.append(stats._start)
        bust.append(stats._bust)
        ppr_boom.append(stats._ppr_boom)
        ppr_start.append(stats._ppr_start)
        ppr_bust.append(stats._ppr_bust)

    df = pd.DataFrame(
        data=zip(player_names, games, boom, start, bust, ppr_boom, ppr_start, ppr_bust),
        columns=BOOM_BUST_COLUMNS,
    )
    df.to_csv("all_boom_bust.csv", index=False)


def main() -> None:
    boom_bust_data = _build_boom_bust_data()
    _create_csv(boom_bust_data)


if __name__ == "__main__":
    main()
