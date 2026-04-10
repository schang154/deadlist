import requests
import pandas as pd
import time

url = "https://nservice.moj.gov.tw/DeadBook/Home/QueryLog"

session = requests.Session()

session.get("https://nservice.moj.gov.tw/deadbook/")

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://nservice.moj.gov.tw/deadbook/",
    "Origin": "https://nservice.moj.gov.tw",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

payload = {
    "qSex": "",
    "qDteDeathYYY": "",
    "qDteDeathMM": "",
    "qDteDeathDD": "",
    "qDeathCity": "",
    "qHeight": "",
}

all_rows = []
    
res = session.post(url, data=payload, headers=headers)

print("Status:", res.status_code)

if res.status_code != 200:
    print(res.text[:300])  # 👉 看錯誤內容

data = res.json()

rows = data.get("data", {}).get("rDeadList", [])

print(rows)

all_rows.extend(rows)

time.sleep(0.3)  # 防封鎖

df = pd.DataFrame(all_rows)

print("Total rows:", len(df))

df.to_csv("csv/raw_death_full.csv", index=False, encoding="utf-8-sig")
