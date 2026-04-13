from pathlib import Path
import logging
import pandas as pd
import requests

BASE_URL = "https://nservice.moj.gov.tw/deadbook/"
API_URL = "https://nservice.moj.gov.tw/DeadBook/Home/QueryLog"
OUTPUT_PATH = Path("./csv/raw_death_full.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": BASE_URL,
    "Origin": "https://nservice.moj.gov.tw",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

PAYLOAD = {
    "qSex": "",
    "qDteDeathYYY": "",
    "qDteDeathMM": "",
    "qDteDeathDD": "",
    "qDeathCity": "",
    "qHeight": "",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def fetch_data() -> pd.DataFrame:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with create_session() as session:
        logger.info("Initializing session...")
        init_res = session.get(BASE_URL, timeout=30)
        init_res.raise_for_status()

        logger.info("Fetching data from API...")
        res = session.post(API_URL, data=PAYLOAD, timeout=30)
        res.raise_for_status()

        data = res.json()
        rows = data.get("data", {}).get("rDeadList")

        if rows is None:
            raise KeyError("Expected key path 'data -> rDeadList' was not found.")

        df = pd.DataFrame(rows)
        df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

        logger.info("Saved %s rows to %s", len(df), OUTPUT_PATH)
        return df


if __name__ == "__main__":
    try:
        df = fetch_data()
        print(f"Fetch completed successfully. Rows fetched: {len(df)}")
    except Exception as exc:
        logger.exception("Fetch failed: %s", exc)
        raise