import typing

import pandas as pd
import requests
from bs4 import BeautifulSoup
from FootballNameMatcher import match_name

from constants import SOS_URLs

MISABBREVIATIONS = {
    "LVR": "LV",
    "JAX": "JAC",
}


def main() -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    for season_type, url in SOS_URLs.items():
        page = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", class_="grid")
        rows = table.find_all("tr")[1:]  # type: ignore
        data = []
        for row in rows:
            cols = row.find_all("td")
            important_data = [col.text for col in cols[0:7]]
            if important_data[0] in MISABBREVIATIONS:
                important_data[0] = MISABBREVIATIONS[important_data[0]]
            data.append(important_data)
        df = pd.DataFrame(data, columns=["TEAM", "QB", "RB", "WR", "TE", "K", "DEF"])
        df.to_csv(f"stats24/sos_{season_type}.csv", index=False)


if __name__ == "__main__":
    main()
