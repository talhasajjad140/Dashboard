# Storm Events Dashboard

A data visualization dashboard built with Streamlit to explore patterns in severe weather events from the NOAA Storm Events Database. This project analyzes storm occurrences, property damage, injuries, and fatalities across different US states and event types.

## How to Run Locally

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

Then run the dashboard:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

- **app.py** — Main Streamlit application with the dashboard layout, filters, and KPI metrics
- **charts.py** — Contains all 10 chart functions (pie, histogram, line, bar, scatter, box, heatmap, area, count, violin)
- **filters.py** — Data loading and filtering logic, including the damage string conversion helper
- **requirements.txt** — All Python dependencies with version pins
- **data/** — Folder for the storm events CSV file
- **notebooks/** — Jupyter notebook for exploratory data analysis

## Dataset

The dataset comes from the **NOAA Storm Events Database**:

- **Source:** https://www.ncei.noaa.gov/stormevents/
- **Format:** CSV file
- **Important:** Do not rename the CSV file — use the filename exactly as downloaded from NOAA

The dataset contains detailed information about severe weather events including:
- Event type (Tornado, Hail, Wind, etc.)
- State and location
- Date and time
- Property and crop damage estimates
- Injuries and fatalities
- Event magnitude

## Key Insights

- Tornado and Hail events are the most frequent severe weather phenomena in the dataset
- Property damage has increased significantly in recent years, correlating with inflation and increased development in storm-prone areas
- Most deaths from severe storms occur in a small number of states with high tornado activity
- There's a strong correlation between event type and the severity of damages and injuries

## Deployment

This dashboard is ready to deploy on **Streamlit Community Cloud**:

1. Push your GitHub repo with the code and data folder
2. Go to https://share.streamlit.io
3. Connect your GitHub account and select this repo
4. Streamlit will deploy automatically

**Live App Link:** [Your deployed link here]

## Technologies Used

- **Streamlit** — Web framework for data apps
- **Pandas** — Data manipulation and analysis
- **NumPy** — Numerical computing
- **Matplotlib & Seaborn** — Data visualization
