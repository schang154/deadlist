import pandas as pd
import json
import logging
from datetime import datetime
from constants import (
    FOCUS_REGIONS, DEFAULT_START_DATE, SOURCE_NAME, 
    METADATA_PATH, DATE_COL, COUNTY_COL
)

logger = logging.getLogger(__name__)

def load_previous_metadata() -> dict:
    default_metadata = {
        "last_pull_date": "Unknown",
        "row_count": 0,
        "previous_row_count": 0,
        "new_rows": 0,
        "source": SOURCE_NAME,
        "focus_region_start_date": DEFAULT_START_DATE,
        "focus_region_counts": {region: 0 for region in FOCUS_REGIONS},
        "focus_region_previous_counts": {region: 0 for region in FOCUS_REGIONS},
    }

    if not METADATA_PATH.exists():
        return default_metadata

    try:
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            old_metadata = json.load(f)

        if isinstance(old_metadata, dict):
            merged = {**default_metadata, **old_metadata}

            merged["focus_region_counts"] = {
                region: old_metadata.get("focus_region_counts", {}).get(region, 0)
                for region in FOCUS_REGIONS
            }
            merged["focus_region_previous_counts"] = {
                region: old_metadata.get("focus_region_previous_counts", {}).get(region, 0)
                for region in FOCUS_REGIONS
            }
            return merged

    except Exception as exc:
        logger.warning("Failed to load previous metadata: %s", exc)

    return default_metadata


def compute_focus_region_counts(df: pd.DataFrame) -> dict:

    df_focus = df.copy()
    df_focus[DATE_COL] = pd.to_datetime(df_focus[DATE_COL], errors="coerce")
    invalid_dates = df_focus[DATE_COL].isna().sum()
    logger.info("Invalid %s values after parsing: %s", DATE_COL, invalid_dates)

    filtered_df = df_focus[
        (df_focus[DATE_COL] >= pd.to_datetime(DEFAULT_START_DATE)) &
        (df_focus[COUNTY_COL].isin(FOCUS_REGIONS))
    ]

    counts = filtered_df[COUNTY_COL].value_counts().to_dict()

    focus_region_counts = {
        region: int(counts.get(region, 0))
        for region in FOCUS_REGIONS
    }

    return {
        "focus_region_start_date": DEFAULT_START_DATE,
        "focus_region_counts": focus_region_counts,
    }

def build_metadata(clean_df: pd.DataFrame, previous_metadata: dict) -> dict:
    pull_time = datetime.now().strftime("%Y-%m-%d")
    previous_row_count = int(previous_metadata.get("row_count", 0))

    previous_focus_counts = {
        region: int(previous_metadata.get("focus_region_counts", {}).get(region, 0))
        for region in FOCUS_REGIONS
    }

    current_focus_data = compute_focus_region_counts(clean_df)

    metadata = {
        "last_pull_date": pull_time,
        "row_count": int(len(clean_df)),
        "previous_row_count": previous_row_count,
        "new_rows": int(len(clean_df) - previous_row_count),
        "source": SOURCE_NAME,
        "focus_region_start_date": current_focus_data["focus_region_start_date"],
        "focus_region_counts": current_focus_data["focus_region_counts"],
        "focus_region_previous_counts": previous_focus_counts,
    }

    return metadata

def save_metadata(metadata: dict) -> None:
    METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    logger.info("Metadata saved to %s", METADATA_PATH.resolve())
    logger.info("Metadata content: %s", metadata)