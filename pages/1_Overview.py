import streamlit as st
import pandas as pd
from components import render_sidebar, render_case_table, render_footer
from utils import (
    load_data, get_data_metadata, build_hidden_columns,
    filter_dataframe, get_latest_date,
    init_lang, set_lang_selector, t
)
from constants import CSV_FILE, DATE_COL, DEFAULT_START_DATE, FOCUS_REGIONS


st.set_page_config(page_title="Overview", layout="wide")

init_lang()
set_lang_selector()
metadata = get_data_metadata()

st.title(t("page_overview_title"))

COLUMNS_TO_SHOW = [
    "發現日期", "編號", "性別", "姓名", "年齡範圍",
    "區域", "縣市", "發現地址", "死亡原因", "承辦檢察署",
    "存放地", "身材描述", "身高", "身體特徵", "衣著特徵",
    "隨身物品", "死亡方式", "報驗機關", "承辦單位", "e化案號",
]

DETAIL_COLUMNS = [
    "姓名", "區域", "承辦檢察署", "存放地", 
    "身材描述", "身高", "身體特徵", "衣著特徵",
    "隨身物品", "死亡方式", "報驗機關", "承辦單位", "e化案號",
]

df = load_data(CSV_FILE, DATE_COL, COLUMNS_TO_SHOW)

sidebar_state = render_sidebar(df, DEFAULT_START_DATE, use_defaults=False)

filtered_df = filter_dataframe(df, DATE_COL, sidebar_state["selected_date"],
                               sidebar_state["selected_regions"], 
                               sidebar_state["selected_cities"]
                               )

hidden_cols = build_hidden_columns(DETAIL_COLUMNS, 
                                   sidebar_state["show_details"]
                                   )

def get_total_cases(df):
    return len(df)

def get_new_last_7_days(df, date_col):
    if df.empty:
        return 0
    cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=7)
    dates = pd.to_datetime(df[date_col], errors="coerce")
    return int((dates >= cutoff).sum())

def get_focus_region_cases(df, focus_cities=FOCUS_REGIONS):
    if df.empty or "縣市" not in df.columns:
        return 0
    return int(df["縣市"].isin(focus_cities).sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric(t("metric_total_case_count"), get_total_cases(filtered_df))
col2.metric(t("metric_last_7_days_count"), get_new_last_7_days(filtered_df, DATE_COL))
col3.metric(t("metric_focus_case_count"), get_focus_region_cases(filtered_df), help=t("metric_focus_region_cases_help"))
col4.metric(t("metric_latest_date"), get_latest_date(filtered_df, DATE_COL))

st.subheader("Recent Trend")
if not filtered_df.empty:
    trend_df = filtered_df.copy()
    trend_df[DATE_COL] = pd.to_datetime(trend_df[DATE_COL], errors="coerce")
    daily_counts = (
        trend_df.dropna(subset=[DATE_COL])
        .groupby(trend_df[DATE_COL].dt.date)
        .size()
    )
    st.line_chart(daily_counts)
else:
    st.info("No data available.")

st.subheader("Recent Updates")

render_case_table(filtered_df.head(10), hidden_cols)

if metadata["last_pull_date"] == "Unknown":
    st.warning("Metadata not found. Last update date is unavailable.")
else:
    render_footer(metadata["last_pull_date"], metadata["source"])