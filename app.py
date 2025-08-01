### Preparing the environment for the Streamlit app ###
# Importing necessary libraries
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import statsmodels
import streamlit as st

# Loading the dataset
df = pd.read_csv('./vehicles_us.csv')










### Cleaning the dataset: ###

# Convert 'date_posted' column to datetime format
df['date_posted'] = pd.to_datetime(df['date_posted'])
# Convert 'model_year' and 'cylinders' to 'Int64' format
df['model_year'] = df['model_year'].astype('Int64')
df['cylinders'] = df['cylinders'].astype('Int64')

# Filling missing values felevant columns
# Fill missing values for 'cylinders' with the most common value in the column
df['cylinders'] = df['cylinders'].fillna(df['cylinders'].mode()[0])
# Fill missing values for 'paint_color' with 'unknown'
df['paint_color'] = df['paint_color'].fillna('unknown')
# Updating 'is_4wd' column and renaming it to 'drivetrain':
df['is_4wd'] = df['is_4wd'].fillna('AWD')
df['is_4wd'] = df['is_4wd'].replace({1.0 : '4WD'})
df.rename(columns={'is_4wd': 'drivetrain'}, inplace=True)

# Removing listings that have their price set below 300 as likely errors or spam
df = df[(df['price'] > 300)]

# Creating 'brand' column, which contains the first word of the 'model' column
df['brand'] = df['model'].str.split().str[0]



## Creating filters for treating outliers

# Creating a 99th percentile threshold for removing outliers in the 'price' column
price_threshold = df['price'].quantile(0.99)
df_filtered_pr = df[df['price'] < price_threshold]

# Filtering by 99th percentile of odometer
odometer_cutoff = df_filtered_pr['odometer'].quantile(0.99)
df_filtered_pr_od = df_filtered_pr[df_filtered_pr['odometer'] <= odometer_cutoff]

# Removing vehicles older than 1960 to exclude outliers in 'model_years' (0 or 1 car per year)
df_filtered_pr_year = df_filtered_pr[df_filtered_pr['model_year'] >= 1960]








### Streamlit app ###
# Setup and intro
st.set_page_config(layout="wide")
st.title('Car sales dashboard')
st.markdown('''
         **This app allows to explore which factors impact prices for used cars**
         Below you can see:
         1. A **dashboard** allowing to explore how different categorical characteristics impact the price.
         2. A **histogram** showing correlation between price and vehicle's age.
         3. A **scatterplot** showing correlation between price and vehicle's mileage.
        
         By default, extreme outliers by price (top %1) are excluded. To see the whole price range, please uncheck the checkbox below.
         ''')

# Checkbox to exclude price outliers from the plot
exclude_outliers = st.checkbox(
    'Exclude outliers (top %1 by price)',
    value=True,
    key='exclude_price_outliers'
)
chosen_df = df_filtered_pr if exclude_outliers else df




# Dashboard: box plot of price distributions by categorical characteristics
#   Allows to compare price distributions by a chosen parameter
#   Allows to exclude outliers based on a checkbox selection

st.header('1. Price distribution by different vehicle characteristics')
st.markdown('''
            Using this dashboard you can explore how the following characteristics impact vehicle's price
            (to switch between presentations, please use the selector below):
            - condition,
            - brand,
            - type (sedan, coupe, bus, etc),
            - fuel type,
            - transmission type,
            - drivetrain type (4WD vs AWD),
            - number of cylinders.
            \n\n
            Each category is presented as a box plot:
            - The boxes represent the price range for middle %50 of all cars in the category.
            - Horizontal lines inside each box represent median price for the category.
            - Dashed horizontal line on the chart represents overall median price for the whole database. 
            \n\n
            Outliers by price (top %1) are excluded by default. To see the whole range, please uncheck the checkbox below.
    ''')


# Creating a parameter for choosing the column for the x-axis
param_to_compare = st.selectbox(
    'Select parameter for comparison',
    options=['brand', 
            'condition', 
            'cylinders', 
            'drivetrain', 
            'fuel', 
            'transmission', 
            'type'],
    index=1,
    key='x_axis_column'
)
# Function for ordering x-axis based on median price for selected parameter
def conditions_order(df, param):
    return df.groupby(param)['price'].median().sort_values().index.tolist()


# Creating the box plot
fig = px.box(
        chosen_df,
        y='price', 
        x=param_to_compare, 
        color=param_to_compare, 
        category_orders={param_to_compare: conditions_order(chosen_df, param_to_compare)},
        title=f'Price distribution by vehicle\'s {str(param_to_compare)}',
        height=600,
    )
fig.add_hline(y=chosen_df['price'].median(), line_dash='dash',
              annotation_text='Median', annotation_position='top right',
              line_color='green')
st.write(fig)






# Second chart: histogram of price distribution by 'model_year'
#   Allows to filter by vehicle's condition

st.header('2. Price distribution by vehicle\'s age')
st.markdown('''
            This histogram shows the median car prices by year of manufacture.
            Cars older tham 1960 are exluded to remove outliers (0-2 cars per year)
            \n\n
            To filter by vehicle's condition, please use the selector below.
            
    ''')



# Filtering out rows with 'model_year' less than 1960 to exclude outliers (0 or 1 car per year)
df_filtered_year = chosen_df[chosen_df['model_year'] > 1960]

# Creating a multiselect box for filtering by vehicle's condition
# The conditions are sorted from worst to best
conditions = ['salvage', 'fair', 'good', 'excellent', 'like new', 'new']
st.multiselect(
    'Select vehicle condition(s) to filter by',
    options=conditions,
    default=conditions,
    key='condition_filter'
)
df_filtered_year = df_filtered_year[df_filtered_year['condition'].isin(st.session_state.condition_filter)]

# Creating the histogram
fig = px.histogram(
        df_filtered_year,
        y='price', 
        x='model_year', 
        histfunc='avg',
        title=f'Price distribution by vehicle\'s year of manufacture',
        height=600,
    )
st.write(fig)





# Third chart: scatterplot of price distribution by 'odometer'

st.header('3. Price distribution by vehicle\'s mileage (odometer reading)')
st.markdown('''
            This scatterplot shows distribution of car prices by odometer reading at the time of sale.
            Extreme outliers by mileage (top %1) are excluded.
            ''')

# Creating the scatterplot
# Price distribution by 'odometer'

# Calculate 99th percentile of odometer
odometer_cutoff = chosen_df['odometer'].quantile(0.99)

# Filter the DataFrame
df_filtered_odometer = chosen_df[chosen_df['odometer'] <= odometer_cutoff]

fig = px.scatter(
    df_filtered_odometer, 
    x='odometer', 
    y='price', 
    opacity=0.2,
    trendline='ols',
    title="Price distribution by odometer", 
    height=600)
st.write(fig)

