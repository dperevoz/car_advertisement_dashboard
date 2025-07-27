### Preparing the environment for the Streamlit app ###
# Importing necessary libraries
import pandas as pd
import plotly_express as px
import streamlit as st

# Loading the dataset
df = pd.read_csv('./vehicles_us.csv')










### Cleaning the dataset: ###
# Convert 'date_posted' column to datetime format
df['date_posted'] = pd.to_datetime(df['date_posted'])

# Removing the 'is_4wd' column from the dataset
#   It contains only values '1.0' and 'NaN. 
#   So we cannot compare 4WD with non-4WD cars, as we don't know if any car is non-4WD for certain. 
#   That means that we cannot use this column for any analysis.
df = df.drop(columns=['is_4wd'])

# Replacing 'NaN' with 'not_listed' for non-numeric columns
for column in df.columns:
    if df[column].dtype == 'object':
        df[column] = df[column].fillna('not_listed')

# Creating 'brand' column, which contains the first word of the 'model' column
def get_brand(model):
    return model.split()[0]
df['brand'] = df['model'].str.split().str[0]

# Removing listings that have their price set below 1000
#   These listings are likely to be errors or spam.
df = df[(df['price'] > 1000)]










### Streamlit app ###
# Setup
st.set_page_config(layout="wide")
st.title('Car sales dashboard')



# First chart: violin plot of price distributions by categorical parameters
#   Allows to compare price distributions by a chosen parameter
#   Allows to exclude outliers based on a checkbox selection
st.header('1. Price distribution by different parameters')
st.markdown('''
    This chart shows the distribution of prices by brand, type or condition. \n
    The x-axis is sorted by the median price.
    Outliers are excluded by default, but this can be changed by unchecking the box below. \n
    ''')

# Creating a parameter for choosing the column for the x-axis
param_to_compare = st.selectbox(
    'Select parameter for comparison',
    options=['brand', 'type', 'condition'],
    index=0,
    key='x_axis_column'
)
# Function for ordering x-axis based on median price for selected parameter
def conditions_order(df, param):
    return df.groupby(param)['price'].median().sort_values().index.tolist()

# Checkbox to exclude outliers from the plot
# We will use 90th percentile as a threshold for outliers
price_threshold = df['price'].quantile(0.9)
df_filtered = df[df['price'] < price_threshold]
exclude_outliers = st.checkbox(
    'Exclude outliers',
    value=True,
    key='exclude_outliers'
)
chosen_df = df_filtered if exclude_outliers else df

# Creating the violin plot
fig = px.violin(
        chosen_df,
        y='price', 
        x=param_to_compare, 
        color=param_to_compare, 
        category_orders={param_to_compare: conditions_order(chosen_df, param_to_compare)},
        title=f'Price distribution by vehicle\'s {str(param_to_compare)}',
        height=600,
    )
st.write(fig)



# Second chart: histogram of price distribution by 'model_year'
#   Allows to filter by vehicle's condition

st.header('2. Price distribution by year of manufacture')
st.markdown('''
    This chart shows the distribution of prices by year of manufacture.
    ''')

# Filtering out rows with 'model_year' less than 1960 to exclude outliers (0 or 1 car per year)
df_by_year = df[df['model_year'] > 1960]

# Creating a multiselect box for filtering by vehicle's condition
# The conditions are sorted from worst to best
conditions = ['salvage', 'fair', 'good', 'excellent', 'like new', 'new']
st.multiselect(
    'Select vehicle condition(s) to filter by',
    options=conditions,
    default=conditions,
    key='condition_filter'
)
df_by_year = df_by_year[df_by_year['condition'].isin(st.session_state.condition_filter)]

# Creating the histogram
fig = px.histogram(
        df_by_year,
        y='price', 
        x='model_year', 
        histfunc='avg',
        title=f'Price distribution by vehicle\'s year of manufacture',
        height=600,
    )
st.write(fig)


