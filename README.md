# Ocean Waste Management — Data Analytics Project

This repository is arranged as a staged academic data analytics project, following the six-folder layout shown in the reference repository.

## Project structure

1. **01_Project_Proposal** — project proposal and report.
2. **02_Data_Collection** — original ocean-waste source data and collection notes.
3. **03_Data_Cleaning** — cleaning script, cleaned data, and validation notes.
4. **04_Data_Analysis** — statistical analysis script, analyzed data, and findings.
5. **05_Data_Visualization** — visualization script and generated chart workbook.
6. **06_Dashboard** — Power BI dashboard and dashboard notes.

## Workflow

Raw data → cleaning and validation → statistical analysis → visualizations → Power BI dashboard.

## Data scope

The supplied project workbook covers annual ocean-waste measures from 1900–2026. Values and calculations should be interpreted according to the source workbook and project report. Do not infer AQI, country, city, or geographic coordinates unless those fields are supplied by a documented source.

## Running the Python workflow

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the scripts from the project root, adjusting file paths to the files in the numbered folders:

```bash
python 03_Data_Cleaning/clean_data_script.py
python 04_Data_Analysis/data_analysis_script.py
python 05_Data_Visualization/data_visualization_script.py
```

**Note about binary source files:** The original ZIP includes Excel, Word, PDF, and Power BI binary files. The GitHub integration used for this update can create text files but cannot transfer those binary attachments directly. The folder READMEs list the exact original filenames to place in each folder; the originals remain in your uploaded ZIP.
