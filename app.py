import streamlit as st
import pandas as pd
import plotly.express as px

# Setup Page
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("COVID-19 Visualization Dashboard")
st.markdown("""
This dashboard visualizes COVID-19 data including cases, deaths, and vaccinations across the world.
Data is sourced from Our World in Data.
""")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_covid_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file 'cleaned_covid_data.csv' not found. Please ensure data preprocessing has been run.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Options")

# Date Filter
min_date = df['date'].min()
max_date = df['date'].max()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Country Filter
all_countries = sorted(df['location'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    all_countries,
    default=["United States", "United Kingdom", "India", "Germany", "Brazil"]
)

# Metric Selection
metric = st.sidebar.selectbox(
    "Select Metric for Analysis",
    ["total_cases", "new_cases", "total_deaths", "people_vaccinated", "vaccination_rate"]
)

# Apply Filters
filtered_df = df[
    (df['date'] >= start_date) & 
    (df['date'] <= end_date) & 
    (df['location'].isin(selected_countries))
]

# Row 1: Line Charts
st.subheader(f"Trends: {metric.replace('_', ' ').title()}")
if not filtered_df.empty:
    fig_line = px.line(
        filtered_df, 
        x='date', 
        y=metric, 
        color='location',
        title=f"{metric.replace('_', ' ').title()} Over Time",
        labels={metric: metric.replace('_', ' ').title(), 'date': 'Date'}
    )
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("Please select at least one country to view trends.")

# Row 2: Heatmap (Choropleth)
st.subheader("Global Heatmap")
date_for_map = st.slider(
    "Select Date for Global View",
    min_value=min_date.date(),
    max_value=max_date.date(),
    value=max_date.date()
)
date_for_map = pd.to_datetime(date_for_map)
map_data = df[df['date'] == date_for_map]

# Remove entries with 0 for better visualization on log scale if needed, 
# but standard linear scale is okay for now.
fig_map = px.choropleth(
    map_data,
    locations="iso_code",
    color=metric,
    hover_name="location",
    color_continuous_scale=px.colors.sequential.Plasma,
    title=f"Global {metric.replace('_', ' ').title()} on {date_for_map.date()}"
)
st.plotly_chart(fig_map, use_container_width=True)

# Row 3: Multivariate Analysis
st.subheader("Cases vs Vaccinations")
st.markdown("Analyzing the relationship between total cases and vaccination rates.")
scatter_date = df['date'].max() # Use latest available data for scatter plot
scatter_data = df[df['date'] == scatter_date]

fig_scatter = px.scatter(
    scatter_data,
    x="vaccination_rate",
    y="total_cases",
    size="population",
    color="continent",
    hover_name="location",
    log_y=True,
    title=f"Total Cases vs Vaccination Rate (Log Scale Y) on {scatter_date.date()}",
    labels={"vaccination_rate": "Vaccination Rate (%)", "total_cases": "Total Cases"}
)
st.plotly_chart(fig_scatter, use_container_width=True)
