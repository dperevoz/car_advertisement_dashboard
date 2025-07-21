import pandas as pd
import plotly_express as px
import altair as alt
import streamlit as st

# Load the dataset
df = pd.read_csv(vehicles_us.csv)

# Display the first few rows of the dataset
print(df.head(10))
