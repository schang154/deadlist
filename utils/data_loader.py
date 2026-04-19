import pandas as pd
import streamlit as st
from typing import List
import json
from constants import METADATA_PATH

def load_data(csv_file: str, date_column: str, columns_to_show: List[str]) -> pd.DataFrame:
    df = pd.read_csv(csv_file)

    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    df = df.dropna(subset=[date_column]).copy()

    df[date_column] = df[date_column].dt.date

    available_columns = [col for col in columns_to_show if col in df.columns]
    df = df[available_columns].copy()

    return df

def get_data_metadata() -> None:
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    return {
        "last_pull_date": "Unknown",
        "row_count": 0,
        "previous_row_count": 0,
        "new_rows": 0,
        "source": "Ministry of Justice, Taiwan | 中華民國法務部",
    }
