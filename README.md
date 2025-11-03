# csv-bar-chart-py
A simple Python project that reads a CSV/TSV file with Ukrainian data (`Область`, `Місто/Район`, `Значення`)
and visualizes it as a bar chart using Pandas and Matplotlib.

## Features
- CLI arguments: `--region`, `--top`, `--sep`, `--horizontal`
- Automatic CSV/TSV delimiter detection
- Saves output chart to `charts/`
- Works with UTF-8 CSV files

## Usage
```bash
python main.py --csv input_data.csv --region "Київська" --top 10