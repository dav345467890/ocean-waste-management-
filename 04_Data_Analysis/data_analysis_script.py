import argparse
import pandas as pd

ANOMALY_LABEL = 'Unrecorded Leakage / Audit Flag'
NO_DATA_LABEL = 'Insufficient Data'


def _year_span(years) -> str:
    years = sorted(int(y) for y in years)
    return str(years[0]) if years[0] == years[-1] else f"{years[0]}-{years[-1]}"


def run_statistical_analysis(cleaned_file_path: str):
    """Print historical summaries, milestone comparisons, correlations, and audit flags."""
    df = pd.read_csv(cleaned_file_path)
    print("=" * 60)
    print("OCEAN WASTE MANAGEMENT: STATISTICAL ANALYSIS REPORT")
    print("=" * 60)

    valid = df.dropna(subset=['ocean_waste_mt'])
    if valid.empty:
        raise ValueError("No valid ocean_waste_mt values are available for analysis.")

    start_year = valid.iloc[0]
    peak_year = valid.loc[valid['ocean_waste_mt'].idxmax()]
    latest_year = valid.iloc[-1]
    growth = (f"{peak_year['ocean_waste_mt'] / start_year['ocean_waste_mt']:.1f}x Expansion"
              if start_year['ocean_waste_mt'] > 0 else "n/a (starting value is zero)")

    print("\n--- 1. Ocean Waste Expansion Summary ---")
    print(f"Initial Ocean Waste ({int(start_year['year'])}): {start_year['ocean_waste_mt']:.2f} MT")
    print(f"Peak Ocean Waste ({int(peak_year['year'])}): {peak_year['ocean_waste_mt']:.2f} MT")
    print(f"Growth Multiple: {growth}")
    print(f"{int(latest_year['year'])} Modeled Ocean Waste: {latest_year['ocean_waste_mt']:.2f} MT")
    if peak_year['anomaly_flag'] == ANOMALY_LABEL:
        print("Note: peak year is flagged as a reporting anomaly; the peak may be inflated.")

    milestone_years = [1900, 1950, 1980, 2000, 2020, 2026]
    cols = ['year', 'plastic_waste_mt', 'ocean_waste_mt', 'waste_collected_mt',
            'waste_recycled_mt', 'management_efficiency_%', 'plastic_share_%',
            'collection_rate_%']
    milestones = df[df['year'].isin(milestone_years)][cols]
    print("\n--- 2. Historical Milestone Summary ---")
    print(milestones.to_string(index=False))
    absent = sorted(set(milestone_years) - set(df['year']))
    if absent:
        print(f"Milestone year(s) not present: {absent}")

    corr_cols = ['ocean_waste_mt', 'plastic_waste_mt', 'fishing_waste_mt',
                 'other_waste_mt', 'waste_collected_mt', 'management_efficiency_%']
    print("\n--- 3. Correlation with Ocean Waste ---")
    print(df[corr_cols].corr()['ocean_waste_mt'].sort_values(ascending=False).to_string())

    anomalies = df[df['anomaly_flag'] == ANOMALY_LABEL][
        ['year', 'ocean_waste_mt', 'expected_ocean_waste_mt', 'reporting_gap_mt']]
    period = f" ({_year_span(anomalies['year'])})" if not anomalies.empty else ""
    print(f"\n--- 4. Reporting Anomaly Audit{period} ---")
    print(anomalies.to_string(index=False) if not anomalies.empty else "No reporting anomalies found.")
    no_data = df[df['anomaly_flag'] == NO_DATA_LABEL]['year'].tolist()
    if no_data:
        print(f"Years that could not be audited: {no_data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze the cleaned ocean waste CSV.")
    parser.add_argument("input", nargs="?", default="cleaned_ocean_waste_data.csv")
    args = parser.parse_args()
    run_statistical_analysis(args.input)
