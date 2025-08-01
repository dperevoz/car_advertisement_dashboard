# 🚗 Car Sales Price Explorer

**Explore how different vehicle characteristics affect used car prices.**

- **GitHub Repository**: [https://github.com/dperevoz/car_advertisement_dashboard/](https://github.com/dperevoz/car_advertisement_dashboard/)
- **Live App on Render**: [https://car-sales-dashboard-52mu.onrender.com/](https://car-sales-dashboard-52mu.onrender.com/)

---

## 📌 Project Description

This interactive Streamlit web app enables users to visually explore how various characteristics (like brand, condition, fuel type, etc.) impact the **resale price** of used cars in the U.S. market.

The app is based on the `vehicles_us.csv` dataset and includes:
1. A dashboard with **box plots** comparing price distributions across different categorical characteristics:
   - condition,
   - brand,
   - type (sedan, coupe, bus, etc),
   - fuel type,
   - transmission type,
   - drivetrain type (4WD vs AWD),
   - number of cylinders.
2. A **histogram** showing average price by vehicle year.
3. A **scatterplot** showing the correlation between price and mileage (odometer reading).

Outliers in price are excluded by default to keep visuals clean but can be reintroduced with a checkbox.

---

## ▶️ How to Use the App

You can try the app directly in your browser (no installation needed):

👉 **[Open the app on Render](https://car-sales-dashboard-52mu.onrender.com/)**

Or run it locally by following these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/dperevoz/car_advertisement_dashboard/
cd car-sales-dashboard
```

### 2. Install Dependencies

Ensure you have Python 3.8+ installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Run the App

To start the Streamlit application, run:

```bash
streamlit run app.py
```

### 4. Explore!

Once launched, the app will open in your browser. You can:
- Select which **vehicle characteristic** to compare with price
- Toggle inclusion of **price outliers**
- Filter results by **vehicle condition**

---

## 🧹 Data Cleaning Summary

Before visualization, the dataset is preprocessed:
- Missing values are filled (e.g., `paint_color`, `cylinders`, `drivetrain`)
- Cars priced under $300 or made before 1960 are excluded
- Outliers in `price`, `odometer`, and `model_year` are filtered out using the 99th percentile

---

## 📂 File Structure


```car-sales-dashboard/
├── README.md # This file
├── app.py # Main Streamlit app script
├── vehicles_us.csv # Dataset used in the app
├── requirements.txt # Dependencies
└── notebooks
   └── EDA.ipynb # Jupyter notebook with full documentation of the analysis process and findings.

```
