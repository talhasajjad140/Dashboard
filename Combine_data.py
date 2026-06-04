import io
import os
import re

import pandas as pd
import requests

base_url = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"

# get directory listing
print("Reading NOAA directory...")
response = requests.get(base_url)
response.raise_for_status()

years = range(1996, 2027)  # 1996 to 2026
all_dfs = []

for year in years:
    matches = re.findall(
        rf'StormEvents_details-ftp_v1\.0_d{year}_c\d+\.csv\.gz',
        response.text
    )
    if matches:
        file_url = base_url + matches[0]
        print(f"Loading {year}...", end=" ")
        try:
            file_resp = requests.get(file_url, timeout=120)
            file_resp.raise_for_status()

            if not file_resp.content.startswith(b"\x1f\x8b"):
                print("❌ Skipped invalid file")
                continue

            df = pd.read_csv(io.BytesIO(file_resp.content), low_memory=False, compression="gzip")
            df["source_year"] = year  # track which year each row came from
            all_dfs.append(df)
            print(f"✅ {len(df)} rows")
        except Exception as e:
            print(f"❌ Failed — {e}")
    else:
        print(f"⚠️ {year} not found")

# combine everything
print("\nCombining all years...")
if not all_dfs:
    raise RuntimeError("No valid NOAA detail files were downloaded.")

final_df = pd.concat(all_dfs, ignore_index=True)
print(f"Total rows: {len(final_df)}")
print(f"Total columns: {len(final_df.columns)}")

# save as single CSV
os.makedirs("data", exist_ok=True)
output_file = "data/StormEvents_combined_1996_2026.csv"
final_df.to_csv(output_file, index=False)
print(f"\n✅ Saved: {output_file}")
print(f"File size: {os.path.getsize(output_file) / (1024*1024):.1f} MB")