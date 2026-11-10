import argparse
import numpy as np
import pandas as pd

ANOMALY_THRESHOLD_MT = 0.05
ANOMALY_LABEL = 'Unrecorded Leakage / Audit Flag'
NO_DATA_LABEL = 'Insufficient Data'
NORMAL_LABEL = 'Normal'

NUMERIC_COLS = ['plastic_waste_mt', 'fishing_waste_mt', 'other_waste_mt',
                'waste_collected_mt', 'waste_recycled_mt', 'ocean_waste_mt',
                'management_efficiency_%']


def clean_ocean_waste_data(file_path: str,
                           output_path: str = "cleaned_ocean_waste_data.csv") -> pd.DataFrame:
    """Validate the raw data and calculate derived metrics and anomaly flags."""
    df = pd.read_csv(file_path)
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(' ', '_', regex=False)
                  .str.replace('(', '', regex=False)
                  .str.replace(')', '', regex=False))

    required = ['year'] + NUMERIC_COLS
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}. Found: {list(df.columns)}")

    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    df = df.drop_duplicates(subset=['year']).sort_values('year').reset_index(drop=True)

    for col in NUMERIC_COLS:
        before_missing = df[col].isna().sum()
        df[col] = pd.to_numeric(df[col], errors='coerce')
        coerced = df[col].isna().sum() - before_missing
        if coerced:
            print(f"Warning: {coerced} non-numeric value(s) in '{col}' treated as missing.")

    df['total_waste_generated_mt'] = (
        df['plastic_waste_mt'] + df['fishing_waste_mt'] + df['other_waste_mt'])
    df['expected_ocean_waste_mt'] = (
        df['total_waste_generated_mt'] - df['waste_collected_mt'])
    df['reporting_gap_mt'] = (
        df['ocean_waste_mt'] - df['expected_ocean_waste_mt']).round(2) + 0.0

    total = df['total_waste_generated_mt']
    collected = df['waste_collected_mt']
    df['collection_rate_%'] = ((collected / total) * 100).where(total > 0).round(2)
    df['recycling_rate_%'] = (
        (df['waste_recycled_mt'] / collected) * 100).where(collected > 0).round(2)
    df['plastic_share_%'] = (
        (df['plastic_waste_mt'] / total) * 100).where(total > 0).round(2)

    gap = df['reporting_gap_mt']
    df['anomaly_flag'] = np.select(
        [gap.isna(), gap.abs() > ANOMALY_THRESHOLD_MT],
        [NO_DATA_LABEL, ANOMALY_LABEL],
        default=NORMAL_LABEL,
    )

    df.to_csv(output_path, index=False)
    flagged = df.loc[df['anomaly_flag'] == ANOMALY_LABEL, 'year'].tolist()
    print(f"Cleaned data saved to '{output_path}'. Records: {len(df)}")
    print(f"Anomaly years flagged: {flagged if flagged else 'none'}")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean the raw ocean waste dataset.")
    parser.add_argument("input", nargs="?", default="Ocean_Waste_Management_1900_2026_excel_data.csv")
    parser.add_argument("output", nargs="?", default="cleaned_ocean_waste_data.csv")
    args = parser.parse_args()
    clean_ocean_waste_data(args.input, args.output)
