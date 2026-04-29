import pandas as pd
import glob
import os

# ── 1. Load all three CSV files from the data folder ──────────────────────────
data_folder = os.path.join(os.path.dirname(__file__), "data")
csv_files = glob.glob(os.path.join(data_folder, "*.csv"))

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in: {data_folder}")

df = pd.concat(
    [pd.read_csv(f) for f in sorted(csv_files)],
    ignore_index=True
)

print(f"✔ Loaded {len(csv_files)} file(s) — {len(df):,} total rows")

# ── 2. Filter for Pink Morsel only ────────────────────────────────────────────
df = df[df["product"] == "pink morsel"]
print(f"✔ After filtering for 'pink morsel': {len(df):,} rows")

# ── 3. Calculate sales (quantity × price) ─────────────────────────────────────
df["sales"] = df["quantity"] * df["price"]

# ── 4. Keep only the required output columns ──────────────────────────────────
output_df = df[["sales", "date", "region"]].copy()

# ── 5. Parse and sort by date ─────────────────────────────────────────────────
output_df["date"] = pd.to_datetime(output_df["date"])
output_df = output_df.sort_values("date").reset_index(drop=True)

# ── 6. Write the output CSV ───────────────────────────────────────────────────
output_path = os.path.join(data_folder, "processed_sales.csv")
output_df.to_csv(output_path, index=False)

print(f"✔ Output written to: {output_path}")
print(f"\nPreview of processed data:\n{output_df.head(10).to_string(index=False)}")
print(f"\nShape: {output_df.shape[0]:,} rows × {output_df.shape[1]} columns")
print(f"Columns: {list(output_df.columns)}")
print(f"Date range: {output_df['date'].min().date()} → {output_df['date'].max().date()}")
print(f"Regions: {sorted(output_df['region'].unique())}")
