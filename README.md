# Taiwan Unidentified Cases Monitoring Dashboard

End-to-end analytics system for ingesting, cleaning, and monitoring semi-structured public data with interactive visualization and automated alerts.

## 🚧 Project Status

This project is actively under development.

Current capabilities:
- Data pipeline (API ingestion → cleaning → CSV output)
- Interactive Streamlit dashboard with filtering
- Telegram alerts for newly detected cases

Ongoing work:
- Geographic visualization (heatmap, choropleth)
- Trend analysis and anomaly detection
- Dashboard layout and UX improvements

## Project Overview

This project retrieves unidentified case records from a public data source and transforms semi-structured JSON data into a structured dataset for analysis.

The project was inspired by the [original website](https://nservice.moj.gov.tw/deadbook/#), which provides valuable information but has limited support for filtering and exploration. To address this, I developed a more user-friendly interface with additional capabilities for tracking updates and analyzing regional trends.

It was also motivated by a personal interest in following specific cases over time, and later evolved into a reusable analytics system in combination with data ingestion, transformation, visualization, and monitoring.

## Architecture

API (JSON)
   ↓
Data Fetch (Python)
   ↓
Data Cleaning & Standardization
   ↓
Change Detection
   ↓
CSV Storage (intermediate layer)
   ↓
├─ Streamlit Dashboard
└─ Telegram Alerts

## Data Design

The project uses CSV files as an intermediate storage layer between the data processing pipeline and the dashboard.

This design allows:
- separation of data ingestion and visualization
- faster dashboard performance without repeated API calls
- easier inspection and validation of cleaned data
- reproducible snapshots of processed datasets

For the current scale and update frequency, this provides a lightweight and efficient solution.

## Key Features

### Data Pipeline
- Automated ingestion of JSON data from API
- Data cleaning and standardization using Python
- Change detection for newly added records

### Analytics & Visualization
- Streamlit dashboard with filtering and exploration
- Region-based analysis (eastern and coastal areas)
- Time-based tracking of new cases

### Monitoring & Alerts
- Telegram notifications for new case detection
- Focus-region tracking
- Continuous monitoring workflow

## Dashboard Preview

### Overview (in progress)

### Case Explorer
![table](images/table.png)

### Geographic Analysis (in progress)

## Project Structure

project/
├── app.py
├── pages/
├── scripts/
├── data/
│ ├── raw/
│ └── processed/
├── images/
├── requirements.txt
└── README.md

## Next Steps

- Add geographic heatmap and choropleth visualization
- Implement rolling averages and trend analysis
- Add anomaly detection for unusual spikes
- Improve data quality checks
- Enhance dashboard layout and usability
