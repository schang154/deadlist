import streamlit as st
from components import render_sidebar, render_case_table, render_footer
from utils import (
    load_data, get_data_metadata, build_hidden_columns,
    filter_dataframe, get_latest_date,
    init_lang, set_lang_selector, t
)
from constants import (
    CSV_FILE, DATE_COL, 
    DEFAULT_START_DATE, 
    COLUMNS_TO_SHOW
)

st.set_page_config(
    page_title="Case Explorer",
    layout="wide",
)

init_lang()
set_lang_selector()
metadata = get_data_metadata()

st.title(t("page_case_explorer_title"))

DETAIL_COLUMNS = [
    "身材描述", "身高", "身體特徵", "衣著特徵",
    "隨身物品", "死亡方式", "報驗機關", "承辦單位", "e化案號",
]

df = load_data(CSV_FILE, DATE_COL, COLUMNS_TO_SHOW)

sidebar_state = render_sidebar(df, DEFAULT_START_DATE, use_defaults=True)

filtered_df = filter_dataframe(df, DATE_COL, sidebar_state["selected_date"], 
                               sidebar_state["selected_regions"], 
                               sidebar_state["selected_cities"]
                               )

hidden_cols = build_hidden_columns(DETAIL_COLUMNS, 
                                   sidebar_state["show_details"]
                                   )

# -----------------------------
# Metrics
# -----------------------------
col1, col2 = st.columns(2)

col1.metric(
    t("metric_match_case_count"),
    len(filtered_df),
)

col2.metric(
    t("metric_latest_date"),
    get_latest_date(filtered_df, DATE_COL),
)
render_case_table(filtered_df, hidden_cols)

if metadata["last_pull_date"] == "Unknown":
    st.warning("Metadata not found. Last update date is unavailable.")
    
render_footer(metadata["last_pull_date"], metadata["source"])