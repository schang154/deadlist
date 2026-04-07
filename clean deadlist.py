import pandas as pd
from IPython.display import display
import re


REGION_MAP = {
    # 北部 (North)
    '臺灣臺北地方檢察署': '北部', '臺灣新北地方檢察署': '北部', '臺灣士林地方檢察署': '北部',
    '臺灣桃園地方檢察署': '北部', '臺灣新竹地方檢察署': '北部', '臺灣基隆地方檢察署': '北部',
    '臺灣宜蘭地方檢察署': '北部', '法務部法醫研究所': '北部',
    
    # 中部 (Central)
    '臺灣臺中地方檢察署': '中部', '臺灣彰化地方檢察署': '中部', '臺灣南投地方檢察署': '中部',
    '臺灣苗栗地方檢察署': '中部', '臺灣雲林地方檢察署': '中部',
    
    # 南部 (South)
    '臺灣高雄地方檢察署': '南部', '臺灣橋頭地方檢察署': '南部', '臺灣臺南地方檢察署': '南部',
    '臺灣屏東地方檢察署': '南部', '臺灣嘉義地方檢察署': '南部',
    
    # 東部 (East)
    '臺灣花蓮地方檢察署': '東部', '臺灣臺東地方檢察署': '東部',
    
    # 外島 (Outlying Islands)
    '臺灣澎湖地方檢察署': '外島', '福建金門地方檢察署': '外島', '福建連江地方檢察署': '外島',
}

# The 22 official top-level administrative divisions
STANDARD_CITY = [
    '臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市',
    '基隆市', '新竹市', '嘉義市', '新竹縣', '苗栗縣', '彰化縣', 
    '南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', 
    '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

CHINESE_WEEKDAYS = {
    0: "星期一",
    1: "星期二",
    2: "星期三",
    3: "星期四",
    4: "星期五",
    5: "星期六",
    6: "星期日"
}

MODERN_CITYMAME = {
    '臺中縣': '台中市',
    '臺南縣': '台南市',
    '高雄縣': '高雄市',
    '臺北縣': '新北市',
    '桃園縣': '桃園市',
    '新莊市': '新北市'
}

def find_admin_unit(text: str):
    if pd.isna(text): 
        return None
    # We look for 2 characters + the marker
    match = re.search(r'(.{2}[市縣區鄉鎮])', str(text))
    return match.group(1) if match else None

# Create a mapping that forces the "City/County" suffix
def unit_to_full_city(unit: str):
    if '橋頭' in unit: return '高雄市'
    if '士林' in unit: return '臺北市'
    if '法醫' in unit: return '新北市'
    
    # Most Prosecutors offices are "City" level, but some are "County"
    name = unit[2:4].replace('台', '臺')
    
    # List of known Counties (remaining are usually Cities)
    counties = ['屏東', '宜蘭', '花蓮', '臺東', '澎湖', '彰化', '南投', '苗栗', '雲林', '嘉義', '連江', '金門']
    
    if name in counties:
        return f"{name}縣"
    else:
        return f"{name}市"

# Load the dataset
df = pd.read_csv('csv/raw_death_full.csv')

# DeathYYY has min 11, doesn't make sense
df.loc[df['rID'] == "20240322102253615", 'rDteDeathYYY'] = 111
df.loc[df['rID'] == "20240322102253615", 'rTimeOfDiscovery'] = '民國111年09月11日'

# Consilidate reasons
df['Reason'] = df['rReasonA'].str.cat([df['rReasonB'], df['rReasonC'], df['rReasonD']], sep=' ', na_rep='')

# Create Date column
# Apply the +1911 Offset to the Year
# Note: We only add 1911 if the year is already present (not NaN)
df['year_corr'] = df['rDteDeathYYY'] + 1911

# Create the DeathDate column
# pd.to_datetime will return NaT if Year, Month, or Day is missing
df['DeathDate'] = pd.to_datetime(pd.DataFrame({
    'year': df['year_corr'],
    'month': df['rDteDeathMM'],
    'day': df['rDteDeathDD']
}), errors='coerce')

# 4. Generate the Weekday Number (0=Mon, 6=Sun)
df['WeekdayNum'] = df['DeathDate'].dt.weekday

# Strip the time and keep only the YYYY-MM-DD
df['DeathDate'] = df['DeathDate'].dt.date

# 5. Map to Traditional Chinese Weekdays
df['Weekday'] = df['WeekdayNum'].map(CHINESE_WEEKDAYS)

# Create the 'Region' column
df['Region'] = df['rUnitName'].map(REGION_MAP)


#######     Clean up city names      #######

# Modernize the cities in the address and standardize 台 to 臺
cols_to_fix = ['rDeathCity', 'rDeathAddr', 'rPlaceOfDiscovery']
df[cols_to_fix] = df[cols_to_fix].replace('台', '臺', regex=True)

# Mapping of old names to new standards
df[cols_to_fix] = df[cols_to_fix].replace(MODERN_CITYMAME, regex=True)

# Extract city from address
df['ExtractedCity'] = df['rDeathAddr'].apply(find_admin_unit)

# Clean up any weird leading/trailing whitespace
df['ExtractedCity'] = df['ExtractedCity'].str.strip()

extracted_compare = df[['rTimeOfDiscovery', 'rDeathCity', 'rDeathAddr', 'ExtractedCity', 'rUnitName']].copy()

# 3. Fill nan city with extracted cities

# Define the filter (the rows where rDeathCity is null)
mask = (
    extracted_compare['rDeathCity'].isna() |
    (extracted_compare['rDeathAddr'].str.contains('其他', na=False) & 
     extracted_compare['ExtractedCity'].notna())
)

# Use .loc[rows, column] to fill the values directly in the original df
extracted_compare.loc[mask, 'rDeathCity'] = extracted_compare.loc[mask, 'ExtractedCity']

# Fill the rest with the city the unit is in
extracted_compare.loc[:, 'UnitFullCity'] = extracted_compare['rUnitName'].apply(unit_to_full_city)

extracted_compare.loc[extracted_compare['rDeathCity'].isna(), 'rDeathCity'] = extracted_compare.loc[mask, 'UnitFullCity']

# Finalize cities names with unit cities

def finalize_city_name(city_name, unit_name, address, unit_city_name, city_name_set):
  
    # Check if the value is missing, "不詳", "其他", or lacks "市/縣"   
    needs_replace = (
        pd.isna(city_name) or 
        city_name == 'nan' or 
        '不詳' in city_name or 
        '其他' in city_name or 
        (not ('市' in city_name or '縣' in city_name))
    )

    # List of Shilin districts that belong to New Taipei City
    shilin_new_taipei = ['淡水', '八里', '三芝', '石門']

    if needs_replace:
        # --- Special Case: Shilin ---
        if '士林' in unit_name:
            # Look at the address to decide between Taipei or New Taipei
            if any(dist in address for dist in shilin_new_taipei):
                return '新北市'
            else:
                return '臺北市'
        
        # --- General Case ---
        return unit_city_name
    
    # Otherwise (for 鳳山市, 永和市, 剛雄縣, etc.), use the Unit's City
    if city_name not in city_name_set:
        return unit_city_name
    
    # If it already has "市" or "縣" and isn't "不詳/其他", keep it
    return city_name

# Apply to the DataFrame using .loc to avoid the SettingWithCopyWarning
extracted_compare['rDeathCity'] = extracted_compare.apply(
    lambda row: finalize_city_name(
        row['rDeathCity'], 
        row['rUnitName'], 
        row['rDeathAddr'], 
        row['UnitFullCity'],
        STANDARD_CITY
    ), 
    axis=1
)

df.loc[:, 'rDeathCity'] = extracted_compare['rDeathCity']

# Convert both to sets for easy comparison
generated_set = set(df['rDeathCity'].unique())
standard_set = set(STANDARD_CITY)

# 1. Non-standard values currently in your data (The "Clean-up" List)
extra_in_data = generated_set - standard_set

# 2. Standard cities that are completely missing from your data
missing_from_data = standard_set - generated_set

print(f"--- Comparison Results ---")
print(f"Non-standard values found in Data: {sorted(list(extra_in_data))}")
print(f"Standard cities NOT present in Data: {sorted(list(missing_from_data))}")
print(df[df['rDeathCity'].isna()][['rUnitName', 'rDeathAddr']])

# Drop the old columns
df.drop(columns=['rDteDeathYYY', 'rDteDeathMM', 'rDteDeathDD', 'rReasonA', 'rReasonB', 'rReasonC', 'rReasonD', 'rDetailsViewed', 'year_corr', 'ExtractedCity'], inplace=True)

df.to_csv('csv/death_full.csv', index=False, encoding='utf-8-sig')

df_chinese_column = df.rename(columns={
  'rSerial': '序號', 
  'rID': '編號', 
  'rSex': '性別', 
  'rDead': '姓名', 
  'rSage': '年齡範圍下限', 
  'rEage': '年齡範圍上限', 
  'rAgeRange': '年齡範圍',
  'rDeathCity': '縣市', 
  'rDeathAddr': '發現地址', 
  'rPlaceOfDiscovery': '發現地', 
  'rDteDeathYYY': '發現年',
  'rDteDeathMM': '發現月', 
  'rDteDeathDD': '發現日', 
  'DeathDate': '發現日期',
  'rTimeOfDiscovery': '發現日期民國', 
  'rSize': '身材描述',
  'rSHeight': '身高下限',
  'rEHeight': '身高上限', 
  'rHeightRange': '身高', 
  'rBody': '身體特徵', 
  'rDress': '衣著特徵', 
  'rThings': '隨身物品', 
  'rDeathType': '死亡方式',
  'Reason': '死亡原因', 
  'rPlace': '存放地', 
  'rUnitID': '承辦檢察署ID',
  'rUnitName': '承辦檢察署', 
  'rNoteUnit': '報驗機關', 
  'rECaseNo': 'e化案號', 
  'rHandlingUnit': '承辦單位',
  'Region': '區域',
  'Weekday': '周日',
  'WeekdayNum': '周日數字'
})

# Saves directly to your project folder
df_chinese_column.to_csv('csv/death_full_chinese_column.csv', index=False, encoding='utf-8-sig')