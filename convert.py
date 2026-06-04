import pandas as pd

print("Reading CSV...")
df = pd.read_csv("data/StormEvents_combined_1996_2026.csv", low_memory=False)
print(f"Rows loaded: {len(df):,}")

print("Converting to parquet...")
df.to_parquet("data/StormEvents_combined_1996_2026.parquet", index=False)
print("✅ Done! Parquet file saved.")