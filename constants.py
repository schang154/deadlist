from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "csv"
CSV_FILE = DATA_DIR / "death_full_chinese_column.csv"
METADATA_PATH = DATA_DIR / "data_metadata.json"
RAW_OUTPUT_PATH = DATA_DIR / "raw_death_full.csv"
CLEAN_OUTPUT_PATH = DATA_DIR / "death_full.csv"
CLEAN_CHINESE_OUTPUT_PATH = DATA_DIR / "death_full_chinese_column.csv"

DATE_COL = "發現日期"
COUNTY_COL = "縣市"
DEFAULT_START_DATE = "2025-07-22"
FOCUS_REGIONS = ["宜蘭縣", "花蓮縣", "臺東縣", "屏東縣"]
SOURCE_NAME = "Ministry of Justice, Taiwan | 中華民國法務部"