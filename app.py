import streamlit as st
import pandas as pd

# Set Page Config
st.set_page_config(page_title="台灣無名屍名單", layout="wide")

st.title("📊 台灣無名屍名單")

# 1. Load Data (Using cache so it's fast)
@st.cache_data
def load_data(csv_file: str, date_column: str):
    df = pd.read_csv(csv_file) # Point to your actual file
    df[date_column] = pd.to_datetime(df[date_column])
    return df

df = load_data('csv/death_full_chinese_column.csv', '發現日期')

# Define which columns to hide by their names
cols_to_show = ['發現日期', '編號', '性別', '姓名', '年齡範圍',
       '區域', '縣市', '發現地址', '死亡原因', '承辦檢察署', 
       '存放地', '身材描述', '身高', '身體特徵', '衣著特徵',
       '隨身物品', '死亡方式',  '報驗機關',
       '承辦單位', 'e化案號'  
]

# Strip the time and keep only the YYYY-MM-DD
df['發現日期'] = df['發現日期'].dt.date

df = df[cols_to_show]

####################           Sidebar           ####################
st.sidebar.header("篩選選項")

# Date Slicer
min_date = pd.to_datetime('2025-07-22').date()
selected_date = st.sidebar.date_input("發現日期:", min_date)

# Region/City Logic
# (We handle the 'Eastern OR Pingtung' logic automatically)
# toogle_pingtung = st.sidebar.toggle("包括【屏東縣】", value=True)
toggle_show_details = st.sidebar.toggle("顯示其他細節", value=False)

# 1. Region Filter
all_regions = sorted(df['區域'].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "選擇區域:", 
    options=all_regions, 
    default=["北部", "南部", "東部"]
)

# 2. Dynamic City Filter (Linked to Region)
default_cities = []
if not selected_regions:
    default_cities = []
else:
    if "北部" in selected_regions:
        default_cities.append("宜蘭縣")
    
    if "東部" in selected_regions:
        default_cities.extend(["花蓮縣", "臺東縣"])
    
    if "南部" in selected_regions:
        default_cities.append("屏東縣")

available_cities = sorted(df[df['區域'].isin(selected_regions)]['縣市'].unique().tolist()) if selected_regions else sorted(df['縣市'].unique().tolist())

selected_cities = st.sidebar.multiselect(
    "選擇縣市:", 
    options=available_cities,
    default=[c for c in default_cities if c in available_cities] # ensuring default are in the list
)

# In the sidebar
st.sidebar.markdown("[各縣市無名屍業務承辦聯絡方式](https://nservice.moj.gov.tw/DeadBook/Upload/tel_directory.pdf)")

############################################################

# --- Apply Filtering Logic ---
# Start with a true mask
mask = pd.Series([True] * len(df))

if selected_regions:
    mask &= df['區域'].isin(selected_regions)

if selected_cities:
    # Note: We use '|' logic if you want Eastern OR Pingtung specifically
    # but the multiselect naturally handles multiple selections.
    mask &= df['縣市'].isin(selected_cities)

# Date Filter (your 2025-07-22 threshold)
mask &= (df['發現日期'] > selected_date)

filtered_df = df[mask]

###### For hidden columns - Define which columns to hide

hidden_cols = [
    '身材描述', '身高', '身體特徵', '衣著特徵',
    '隨身物品', '死亡方式',  '報驗機關',
    '承辦單位', 'e化案號'  
    ] if not toggle_show_details else []

# 4. Display Metrics
col1, col2 = st.columns(2)
col1.metric("符合條件案件數量", len(filtered_df))
col2.metric("最近一筆", str(filtered_df['發現日期'].max()))

# 5. The Interactive Table
# Streamlit has a built-in interactive dataframe with search and sort
st.dataframe(
    filtered_df, 
    column_config={col: None for col in hidden_cols}, # Hides them if in the list
    use_container_width=True, 
    hide_index=True
)

# 6. Download Button
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("匯出CSV", data=csv, file_name="filtered_death_list.csv")