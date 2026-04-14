import streamlit as st
from utils import init_lang, set_lang_selector, t, get_data_metadata
from components import render_footer

st.set_page_config(
    page_title="Taiwan Unidentified Case Monitor",
    layout="wide",
)

init_lang()
set_lang_selector()
metadata = get_data_metadata()

st.title(t("app_title"))
st.caption(t("app_subtitle"))

st.subheader(t("page_home_title"))
st.markdown("""
This project retrieves unidentified case records from a public data source and transforms semi-structured JSON data into a structured dataset for analysis.

The original website provides access to the data but is not optimized for filtering, exploration, or continuous monitoring. This project improves accessibility by introducing a user-friendly interface, structured data processing, and analytical capabilities.

It was initially motivated by a personal need to follow specific cases, and later evolved into a reusable analytics system combining data ingestion, transformation, visualization, and monitoring.
""")

st.subheader("Project Status")
st.markdown("""
**Current Capabilities**
- API data ingestion and processing pipeline
- Cleaned dataset stored as CSV
- Interactive filtering and case exploration
- Monitoring workflow for newly detected cases

**In Progress**
- Geographic visualization
- Trend analysis
- Dashboard layout and UX improvements
""")

st.subheader("System Workflow")
st.code("""
API (JSON)
   ↓
Data Fetch (Python)
   ↓
Data Cleaning & Standardization
   ↓
Change Detection
   ↓
CSV Storage
   ↓
├─ Streamlit Dashboard
└─ Monitoring / Alerts
""")

st.subheader("Explore the Dashboard")
st.markdown("""
- **Overview**: KPI summary, recent trends, and latest updates  
- **Case Explorer**: filter and inspect detailed records  
- **Geographic Analysis**: regional distribution and location-based patterns  (In progress)
- **Trend Analysis**: time-based monitoring and activity changes  (In progress)
""")

render_footer(metadata["last_pull_date"], metadata["source"])