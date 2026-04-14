import logging
import pandas as pd
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import List
from constants import (
    RAW_OUTPUT_PATH, METADATA_PATH, 
)

BASE_URL = "https://nservice.moj.gov.tw/deadbook/"
API_URL = "https://nservice.moj.gov.tw/DeadBook/Home/QueryLog"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def create_session() -> requests.Session:
    session = requests.Session()

    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": BASE_URL,
        "Origin": "https://nservice.moj.gov.tw",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    session.headers.update(headers)
    return session

def fetch_raw_rows() -> List[dict]:
    payload = {
        "qSex": "",
        "qDteDeathYYY": "",
        "qDteDeathMM": "",
        "qDteDeathDD": "",
        "qDeathCity": "",
        "qHeight": "",
    }

    with create_session() as session:
        logger.info("Initializing session...")
        init_res = session.get(BASE_URL, timeout=30)
        init_res.raise_for_status()

        logger.info("Fetching data from API...")
        res = session.post(API_URL, data=payload, timeout=30)

        if not res.ok:
            logger.error("Status: %s", res.status_code)
            logger.error("Response text: %s", res.text[:2000])
            res.raise_for_status()

        data = res.json()
        rows = data.get("data", {}).get("rDeadList")

        if rows is None:
            raise KeyError("Expected key path 'data -> rDeadList' was not found.")

        return rows
    


def fetch_data() -> pd.DataFrame:
    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = fetch_raw_rows()
    df = pd.DataFrame(rows)

    df.to_csv(RAW_OUTPUT_PATH, index=False, encoding="utf-8-sig")

    logger.info("RAW_OUTPUT_PATH: %s", RAW_OUTPUT_PATH.resolve())
    logger.info("METADATA_PATH: %s", METADATA_PATH.resolve())
    logger.info("Saved %s rows to %s", len(df), RAW_OUTPUT_PATH)

    return df


if __name__ == "__main__":
    try:
        df = fetch_data()
        print(f"Fetch completed successfully. Rows fetched: {len(df)}")
    except Exception as exc:
        logger.exception("Fetch failed: %s", exc)
        raise
