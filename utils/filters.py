import pandas as pd
from typing import List



def filter_dataframe(df: pd.DataFrame, date_column: str, selected_date: str, 
                     selected_regions: List[str], selected_cities: List[str]) -> pd.DataFrame:
  mask = pd.Series(True, index=df.index)

  if selected_regions:
      mask &= df["區域"].isin(selected_regions)

  if selected_cities:
      mask &= df["縣市"].isin(selected_cities)

  # Use >= so the selected date is included
  mask &= df[date_column] >= selected_date

  return df.loc[mask].copy()


def build_hidden_columns(detail_columns: List[str], show_details: bool) -> List[str]:
  return [] if show_details else detail_columns


def get_latest_date(df: pd.DataFrame, date_column: str) -> str:
  if df.empty or date_column not in df.columns:
      return "-"

  latest_date = df[date_column].max()
  return str(latest_date) if pd.notna(latest_date) else "-"