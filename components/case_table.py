import pandas as pd
import streamlit as st
from typing import List


from utils.i18n_utils import t


def render_case_table(df: pd.DataFrame, hidden_cols: List,) -> None:
  st.dataframe(
      df,
      column_config={col: None for col in hidden_cols},
      use_container_width=True,
      hide_index=True,
  )

  csv_data = df.to_csv(index=False).encode("utf-8-sig")

  st.download_button(
      label=t("button_download_csv"),
      data=csv_data,
      file_name="filtered_death_list.csv",
      mime="text/csv",
  )