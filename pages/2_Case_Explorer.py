import streamlit as st

from components.sidebar import render_sidebar
from components.case_table import render_case_table
from utils.data_loader import load_data
from utils.filters import (
    build_hidden_columns,
    filter_dataframe,
    get_latest_date,
)
from utils.i18n_utils import init_lang, set_lang_selector, t

st.set_page_config(
    page_title="Case Explorer",
    layout="wide",
)

init_lang()
set_lang_selector()

st.title(t("page_case_explorer_title"))

CSV_FILE = "csv/death_full_chinese_column.csv"
DATE_COL = "發現日期"
DEFAULT_START_DATE = "2025-07-22"

COLUMNS_TO_SHOW = [
    "發現日期", "編號", "性別", "姓名", "年齡範圍",
    "區域", "縣市", "發現地址", "死亡原因", "承辦檢察署",
    "存放地", "身材描述", "身高", "身體特徵", "衣著特徵",
    "隨身物品", "死亡方式", "報驗機關", "承辦單位", "e化案號",
]

DETAIL_COLUMNS = [
    "身材描述", "身高", "身體特徵", "衣著特徵",
    "隨身物品", "死亡方式", "報驗機關", "承辦單位", "e化案號",
]

df = load_data(CSV_FILE, DATE_COL, COLUMNS_TO_SHOW,)

sidebar_state = render_sidebar(df, DEFAULT_START_DATE,)

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