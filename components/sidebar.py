import pandas as pd
import streamlit as st
from utils.i18n_utils import t

CONTACT_URL = "https://nservice.moj.gov.tw/DeadBook/Upload/tel_directory.pdf"

REGION_CITY_DEFAULTS = {
    "北部": ["宜蘭縣"],
    "東部": ["花蓮縣", "臺東縣"],
    "南部": ["屏東縣"],
}


def render_sidebar(df: pd.DataFrame, default_start_date: str, 
                   use_defaults: bool = False) -> dict:
    st.sidebar.header(t("sidebar_section_filters"))

    min_date = pd.to_datetime(df['發現日期'], errors="coerce").min().date()
    default_regions = []

    if use_defaults:
        default_regions = ["北部", "南部", "東部"]
        selected_date = st.sidebar.date_input(
            t("sidebar_filter_date"),
            value=pd.to_datetime(default_start_date).date(),
        )
    else:
        selected_date = st.sidebar.date_input(
            t("sidebar_filter_date"),
            value=min_date
        )

    all_regions = sorted(df["區域"].dropna().unique().tolist())

    selected_regions = st.sidebar.multiselect(
        t("sidebar_filter_region"),
        options=all_regions,
        default=[r for r in default_regions if r in all_regions],
    )

    if selected_regions:
        available_cities = sorted(
            df.loc[df["區域"].isin(selected_regions), "縣市"]
            .dropna()
            .unique()
            .tolist()
        )
    else:
        available_cities = sorted(df["縣市"].dropna().unique().tolist())

    default_cities = []
    for region in selected_regions:
        default_cities.extend(REGION_CITY_DEFAULTS.get(region, []))

    selected_cities = st.sidebar.multiselect(
        t("sidebar_filter_county"),
        options=available_cities,
        default=[city for city in default_cities if city in available_cities],
    )

    show_details = st.sidebar.toggle(
        t("sidebar_toggle_show_details"),
        value=False,
    )

    st.sidebar.markdown(
        f"[{t('sidebar_link_county_contacts')}]({CONTACT_URL})"
    )

    return {
        "selected_date": selected_date,
        "selected_regions": selected_regions,
        "selected_cities": selected_cities,
        "show_details": show_details,
    }