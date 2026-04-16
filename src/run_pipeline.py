import os
import logging
import pandas as pd
from dotenv import load_dotenv
from .fetch_data import fetch_data
from .clean_data import main as clean_main
from .metadata import load_previous_metadata, build_metadata, save_metadata
from .notify import maybe_send_alert
from constants import FOCUS_REGIONS, CLEAN_CHINESE_OUTPUT_PATH

logger = logging.getLogger(__name__)
    
def run(send_alert: bool = False) -> None:

    logger.info("Step 1: Fetching data...")
    fetch_data()

    logger.info("Step 2: Cleaning data...")
    clean_main()

    clean_df = pd.read_csv(CLEAN_CHINESE_OUTPUT_PATH)

    logger.info(
        "Step 3: Using cleaned CSV from %s, building metadata...",
        CLEAN_CHINESE_OUTPUT_PATH,
    )
    previous_metadata = load_previous_metadata()
    metadata = build_metadata(clean_df, previous_metadata)

    logger.info("Step 4: Saving metadata...")
    save_metadata(metadata)

    token = os.getenv("TOKEN")
    chat_ids_raw = os.getenv("CHAT_ID", "")
    chat_ids = [cid.strip() for cid in chat_ids_raw.split(",") if cid.strip()]
    target_counties = FOCUS_REGIONS

    logger.info("Step 5: Sending notification...")
    maybe_send_alert(False, token, chat_ids, target_counties, metadata)

if __name__ == "__main__":
    load_dotenv()
    run()
