import time
import typing

import pandas as pd
from bs4 import BeautifulSoup
from FootballNameMatcher.match import match_name
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from constants import AVG_DF_COLUMNS, RANK_DF_COLUMNS, TOTAL_DF_COLUMNS, URLs


def setup_chrome_options() -> Options:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-offer-store-unmasked-wallet-cards")
    chrome_options.add_argument("--disable-offer-upload-credit-cards")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--no-first-run")

    return chrome_options


def download_rank_data() -> None:
    driver = _create_driver()

    for position, url in URLs.items():
        soup = _get_soup_from_desired_page(url, "Ranks", driver)
        table = soup.find("table", {"id": "ranking-table"})
        rows = table.find_all("tr")  # type: ignore
        data = []
        tier = 0
        for row in rows:
            if "tier-row" in row["class"]:
                tier += 1
                pass
            elif "player-row" in row["class"]:
                player_data = []
                cells = row.find_all("td")
                for cell in cells:
                    player_data.append(cell.text)

                # the name and team are in the same cell, so we need to split them
                name, team = _parse_name_team(player_data[2])

                # We only care about column 0 (maybe), columns 2 (NAME + TEAM), and 3-6 (BEST, WORST, AVG, STD.DEV)
                if "RK" in RANK_DF_COLUMNS[position][0]:
                    player_data = (
                        [tier] + [player_data[0]] + [name, team] + player_data[3:7]
                    )
                else:
                    player_data = [name, team] + player_data[3:7]
                if player_data[-1] == "-":
                    player_data[-1] = str(0)
                data.append(player_data)
        df = pd.DataFrame(data, columns=RANK_DF_COLUMNS[position])
        df.to_csv(f"stats24/{position}_rank_stats.csv", index=False)

    driver.quit()


def download_stat_data(stat_type: str) -> None:
    driver = _create_driver()
    button_text = "Stats (Avg.)" if stat_type == "avg" else "Stats (Totals)"
    df_columns = AVG_DF_COLUMNS if stat_type == "avg" else TOTAL_DF_COLUMNS

    for position, url in URLs.items():
        print(f"Downloading {position} data")
        soup = _get_soup_from_desired_page(url, button_text, driver)
        table = soup.find("table", {"id": "ranking-table"})
        rows = table.find_all("tr")  # type: ignore
        tier = 0
        data = []
        for row in rows:
            if "tier-row" in row["class"]:
                tier += 1
                pass
            elif "player-row" in row["class"]:
                player_data = []
                cells = row.find_all("td")
                for cell in cells:
                    player_data.append(cell.text)

                # Base which columns are important based on PPR. If non ppr, only get rank, tier, name, team, and fantasy points
                # else get everything
                if _is_ppr_eligible(position):
                    player_data = player_data[0:1] + player_data[2:]
                else:
                    player_data = player_data[0:1] + player_data[2:4]

                # the name and team are in the same cell, so we need to split them
                name, team = _parse_name_team(player_data[1])
                player_data = [player_data[0], tier, name, team] + player_data[2:]
                data.append(player_data)

        df = pd.DataFrame(data, columns=df_columns[position])
        if stat_type == "avg":
            df.to_csv(f"stats24/{position}_avg_stats.csv", index=False)
        else:
            df.to_csv(f"stats24/{position}_total_stats.csv", index=False)

    driver.quit()


def _is_ppr_eligible(position: str) -> bool:
    if "ppr" in position:
        return True
    if position in ["qb", "def", "k"]:
        return True
    return False


def _create_driver() -> webdriver.Chrome:
    chrome_options = setup_chrome_options()
    service = Service("chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def _get_soup_from_desired_page(
    url: str, page_type: str, driver: webdriver.Chrome
) -> BeautifulSoup:
    driver.get(url)
    # Wait until Fantasy Football Draft Rankings is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h1[text()='Fantasy Football Draft Rankings (2024)']")
        )
    )

    # Click the dropdown button that starts on "Overview"
    try:
        overview_button = driver.find_element(
            By.XPATH, "//button[@type='button']/span[text()='Overview']"
        )
        overview_button.click()
    except NoSuchElementException:
        print("Could not find overview button")
        assert False

    # The dropdown should be open, click the rank option
    try:
        ranks_button = driver.find_element(
            By.XPATH, f"//button[@type='button']/div[text()='{page_type}']"
        )
        ranks_button.click()
    except NoSuchElementException:
        print(f"Could not find {page_type} button")
        assert False

    # Wait until the new page is loaded before getting the source
    time.sleep(2)
    return BeautifulSoup(driver.page_source, "html.parser")


def _parse_name_team(name_team: str) -> typing.Tuple[str, str]:
    start = name_team.find("(")
    end = name_team.rfind(")")
    name = name_team[:start].strip()
    team = name_team[start + 1 : end]
    name = match_name(name)
    assert name is not None
    return name, team


def main() -> None:
    download_rank_data()
    # download_stat_data("avg")
    # download_stat_data("total")


if __name__ == "__main__":
    main()
