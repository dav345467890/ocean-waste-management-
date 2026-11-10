# Ocean Waste Management

An annual-data analytics project covering ocean waste trends from 1900–2026. The repository now includes an interactive Streamlit dashboard based on the supplied project workbook and Power BI reference screenshot.

## Run the dashboard

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Dashboard features

- Year-range and historical-era filters
- Peak ocean waste, collected waste, and recycled waste KPI cards
- Waste composition donut chart
- Management-efficiency gauge
- Annual waste-source and ocean-waste trend chart
- Collected-versus-recycled chart
- Filtered data table and CSV export

## Data accuracy note

The uploaded dataset contains annual waste quantities and management-efficiency values. It does not include AQI readings, country/city fields, or latitude/longitude. The dashboard therefore uses management efficiency instead of AQI and does not invent a geographic map. Add verified location and AQI source data before creating those visuals.

## Data

`data/ocean_waste_dashboard_data.csv` contains the annual records transcribed from the supplied Ocean Waste Management workbook. Units are metric tons (MT), except management efficiency (%).

The supplied project also included a Power BI file and reports in the ZIP archive; the interactive dashboard source in this repository is `app.py`.
