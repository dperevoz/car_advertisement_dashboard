# Car Sales Dashboard

This Streamlit app provides interactive visualizations to explore pricing trends in a used vehicles dataset.

## Run the app

[Link](https://car-sales-dashboard-52mu.onrender.com/) (activating on Render may take time, please be patient)

## Features

1. **Price distribution by user-chosen parameter**  
   - Compare price distributions by brand, type, or condition  
   - Option to exclude outliers (top 10%, excluded by default)  
   - Categories sorted by median price

2. **Price distribution by year of manufacture**  
   - Histogram showing average price by model year  
   - Filter: by vehicle condition

## Dataset preparation

- Loaded from `vehicles_us.csv`
- Converted `date_posted` to datetime
- Filled missing values in categorical columns with `'not_listed'`
- Added a `brand` column extracted from the vehicle model
- Removed listings priced below $1000
- Filtered out extreme outliers by manufacture date (model_year < 1960)

## Requirements

- Python 3.8+
- Libraries:
    `pandas`,
    `plotly_express`,
    `streamlit`
