import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
import seaborn as sns

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="COVID-19 Global Intelligence Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Light Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: #f8fafc;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
        box-shadow: 4px 0 24px rgba(0,0,0,0.02);
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    p, li, label {
        color: #334155;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        border-color: #3b82f6;
    }
    
    /* Charts */
    .plotly-graph-div {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        padding: 1rem;
        border: 1px solid #f1f5f9;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
    }
    
    /* Selectboxes */
    .stSelectbox, .stMultiSelect {
        color: #0f172a;
    }
    
    /* Custom Metric Styling */
    div[data-testid="metric-container"] {
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Color Palette (High Contrast / Professional)
COLORS = {
    "primary": "#0ea5e9",      # Sky Blue
    "secondary": "#6366f1",    # Indigo
    "success": "#10b981",      # Emerald
    "danger": "#ef4444",       # Red
    "warning": "#f59e0b",      # Amber
    "cases": "#0284c7",        # Deep Sky
    "deaths": "#dc2626",       # Deep Red
    "vaccinations": "#059669", # Deep Green
    "bg_dark": "#f8fafc",      # Light Gray (repurposed)
    "bg_card": "#ffffff"       # White
}

PLOTLY_TEMPLATE = "plotly_white"

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('cleaned_covid_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please run data preprocessing first.", icon="🚨")
        st.stop()

df = load_data()

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================
with st.sidebar:
    st.markdown("## 🎛️ Control Center")
    st.markdown("---")
    
    # Date Range Filter
    st.markdown("### 📅 Time Period")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.date_input(
        "Select Date Range",
        value=[max_date - pd.Timedelta(days=365), max_date],
        min_value=min_date,
        max_value=max_date,
        key="date_range"
    )
    
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    else:
        start_date, end_date = pd.to_datetime(min_date), pd.to_datetime(max_date)
    
    st.markdown("---")
    
    # Geography Filter
    st.markdown("### 🌍 Geography")
    all_continents = ['All'] + sorted(df['continent'].dropna().unique().tolist())
    selected_continent = st.selectbox("Continent", all_continents)
    
    if selected_continent != 'All':
        available_countries = sorted(df[df['continent'] == selected_continent]['location'].unique())
    else:
        available_countries = sorted(df['location'].unique())
    
    # Smart defaults
    default_countries = ["United States", "United Kingdom", "India", "Germany", "Brazil"]
    final_defaults = [c for c in default_countries if c in available_countries][:5]
    
    selected_countries = st.multiselect(
        "Focus Countries",
        available_countries,
        default=final_defaults if final_defaults else available_countries[:5]
    )
    
    st.info("💡 Maps show ALL countries. Country selection filters comparison charts.")
    
    st.markdown("---")
    
    # Display Options
    st.markdown("### ⚙️ Options")
    show_log_scale = st.checkbox("Logarithmic Scale", value=False)
    show_per_capita = st.checkbox("Per Capita View", value=False)

# Filter Data
global_mask = (df['date'] >= start_date) & (df['date'] <= end_date)
if selected_continent != 'All':
    global_mask = global_mask & (df['continent'] == selected_continent)

global_df = df[global_mask].copy()

if selected_countries:
    trend_df = global_df[global_df['location'].isin(selected_countries)]
else:
    top_countries = global_df.groupby('location')['total_cases'].max().nlargest(5).index
    trend_df = global_df[global_df['location'].isin(top_countries)]

latest_global = global_df.sort_values('date').groupby('location').last().reset_index()

# =============================================================================
# NAVIGATION
# =============================================================================
selected_tab = option_menu(
    menu_title=None,
    options=["📊 Overview", "📈 Trends", "🗺️ Geographic", "🔬 Analysis", "📉 Statistical", "ℹ️ About"],
    icons=["speedometer2", "graph-up", "globe", "bar-chart", "clipboard-data", "info-circle"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background": "transparent"},
        "icon": {"color": COLORS["primary"], "font-size": "16px"},
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#e2e8f0",
            "border-radius": "8px",
            "padding": "8px 12px",
            "color": "#334155"
        },
        "nav-link-selected": {
            "background": f"linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%)",
            "font-weight": "600",
            "color": "white"
        },
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# VIEW 1: EXECUTIVE OVERVIEW
# =============================================================================
if selected_tab == "📊 Overview":
    st.markdown("# 📊 Executive Overview")
    st.markdown("Global COVID-19 pandemic insights at a glance")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    total_cases = latest_global['total_cases'].sum()
    total_deaths = latest_global['total_deaths'].sum()
    avg_vax_rate = latest_global['vaccination_rate'].mean()
    countries_tracked = latest_global['location'].nunique()
    
    # Delta calculation (vs 30 days ago)
    date_30_ago = end_date - pd.Timedelta(days=30)
    past_data = global_df[global_df['date'] <= date_30_ago]
    if not past_data.empty:
        past_latest = past_data[past_data['date'] == past_data['date'].max()]
        prev_cases = past_latest['total_cases'].sum()
        prev_deaths = past_latest['total_deaths'].sum()
        prev_vax = past_latest['vaccination_rate'].mean()
        
        cases_delta = f"+{((total_cases - prev_cases) / prev_cases * 100):.1f}%" if prev_cases > 0 else None
        deaths_delta = f"+{((total_deaths - prev_deaths) / prev_deaths * 100):.1f}%" if prev_deaths > 0 else None
        vax_delta = f"+{(avg_vax_rate - prev_vax):.1f}%" if prev_vax > 0 else None
    else:
        cases_delta = deaths_delta = vax_delta = None
    
    with col1:
        st.metric("🦠 Total Cases", f"{total_cases:,.0f}", delta=cases_delta)
    with col2:
        st.metric("💀 Total Deaths", f"{total_deaths:,.0f}", delta=deaths_delta, delta_color="inverse")
    with col3:
        st.metric("💉 Avg Vaccination Rate", f"{avg_vax_rate:.1f}%", delta=vax_delta)
    with col4:
        st.metric("🌍 Countries", f"{countries_tracked}")
    
    style_metric_cards(background_color=COLORS["bg_card"], border_left_color=COLORS["primary"], border_size_px=4, box_shadow=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Dashboard Row
    col_map, col_chart = st.columns([2, 1])
    
    with col_map:
        st.markdown("### 🗺️ Global Pandemic Heatmap")
        metric_options = {
            "Total Cases": "total_cases",
            "Deaths": "total_deaths",
            "Vaccination Rate (%)": "vaccination_rate",
            "Cases per Million": "total_cases_per_million"
        }
        selected_metric = st.selectbox("Select Metric", list(metric_options.keys()), key="map_metric")
        metric_col = metric_options[selected_metric]
        
        fig_map = px.choropleth(
            latest_global,
            locations="iso_code",
            color=metric_col,
            hover_name="location",
            hover_data={
                "iso_code": False,
                metric_col: ':,.0f',
                "total_cases": ':,.0f',
                "total_deaths": ':,.0f'
            },
            color_continuous_scale="Turbo",
            template=PLOTLY_TEMPLATE,
            projection="natural earth"
        )
        fig_map.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
                lakecolor="rgba(0,0,0,0)",
                landcolor="#e2e8f0",
                showlakes=False
            ),
            coloraxis_colorbar=dict(
                title=selected_metric,
                thickness=15,
                len=0.7
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)
    
    # 4.3 Top Rankings
    with col_chart: # Changed col_bar to col_chart
        st.subheader("🏆 Top Nations")
        # Ensure we look at global data regardless of selection
        top_df = latest_global.nlargest(10, metric_col).sort_values(metric_col, ascending=True) # Changed map_metric to metric_col
        
        fig_bar = px.bar(
            top_df,
            x=metric_col, # Changed map_metric to metric_col
            y="location",
            orientation='h',
            text_auto='.2s',
            title=f"Leaders in {metric_col.replace('_',' ').title()}", # Changed map_metric to metric_col
            color=metric_col, # Changed map_metric to metric_col
            color_continuous_scale="Viridis",
            template=PLOTLY_TEMPLATE
        )
        fig_bar.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a")
        )
        fig_bar.update_yaxes(title="", tickfont=dict(color="#334155"))
        fig_bar.update_xaxes(tickfont=dict(color="#334155"))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Secondary Row: Timeline
    st.markdown("### 📈 Global Timeline")
    
    global_timeline = global_df.groupby('date').agg({
        'new_cases': 'sum',
        'new_deaths': 'sum',
        'new_cases_smoothed': 'sum'
    }).reset_index()
    
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(
        x=global_timeline['date'],
        y=global_timeline['new_cases_smoothed'],
        name="New Cases (7-day avg)",
        line=dict(color=COLORS["cases"], width=2),
        fill='tozeroy',
        fillcolor=f"rgba(0, 212, 255, 0.2)"
    ))
    
    fig_timeline.update_layout(
        template=PLOTLY_TEMPLATE,
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode='x unified',
        xaxis_title="Date",
        yaxis_title="Daily New Cases",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)

# =============================================================================
# VIEW 2: TRENDS & EVOLUTION
# =============================================================================
elif selected_tab == "📈 Trends":
    st.markdown("# 📈 Temporal Trends & Evolution")
    st.markdown("Analyze pandemic progression over time")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metric Selector
    trend_metrics = {
        "New Cases (Smoothed)": "new_cases_smoothed",
        "New Deaths (Smoothed)": "new_deaths_smoothed",
        "Total Cases": "total_cases",
        "Total Deaths": "total_deaths",
        "Stringency Index": "stringency_index",
        "Reproduction Rate": "reproduction_rate"
    }
    
    selected_trend = st.selectbox("Select Metric", list(trend_metrics.keys()))
    trend_col = trend_metrics[selected_trend]
    
    # Main Trend Line Chart
    fig_trend = px.line(
        trend_df,
        x="date",
        y=trend_col,
        color="location",
        title=f"{selected_trend} Over Time",
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        log_y=show_log_scale
    )
    fig_trend.update_layout(
        height=450,
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0)
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Secondary Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Cumulative Cases (Area Chart)")
        fig_area = px.area(
            trend_df,
            x="date",
            y="total_cases",
            color="location",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_area.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        st.plotly_chart(fig_area, use_container_width=True)
    
    with col2:
        st.markdown("### 💉 Vaccination Progress")
        fig_vax = px.line(
            trend_df,
            x="date",
            y="vaccination_rate",
            color="location",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_vax.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            yaxis_title="Vaccination Rate (%)"
        )
        st.plotly_chart(fig_vax, use_container_width=True)
    
    # Rolling Average Analysis
    st.markdown("### 📉 7-Day Rolling Averages")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Cases Rolling Average
        for country in selected_countries[:3]:  # Limit to top 3 for clarity
            country_data = trend_df[trend_df['location'] == country].copy()
            if 'new_cases' in country_data.columns:
                country_data['rolling_avg'] = country_data['new_cases'].rolling(window=7, min_periods=1).mean()
        
        fig_roll_cases = px.line(
            trend_df,
            x="date",
            y="new_cases_smoothed",
            color="location",
            title="New Cases - Smoothed Trend",
            template=PLOTLY_TEMPLATE
        )
        fig_roll_cases.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_roll_cases, use_container_width=True)
    
    with col4:
        # Deaths Rolling Average
        fig_roll_deaths = px.line(
            trend_df,
            x="date",
            y="new_deaths_smoothed",
            color="location",
            title="New Deaths - Smoothed Trend",
            template=PLOTLY_TEMPLATE
        )
        fig_roll_deaths.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_roll_deaths, use_container_width=True)

# =============================================================================
# VIEW 3: GEOGRAPHIC ANALYSIS
# =============================================================================
elif selected_tab == "🗺️ Geographic":
    st.markdown("# 🗺️ Geographic Distribution Analysis")
    st.markdown("Explore pandemic impact across regions")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Multiple Maps
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🦠 Total Cases by Country")
        fig_map1 = px.choropleth(
            latest_global,
            locations="iso_code",
            color="total_cases",
            hover_name="location",
            color_continuous_scale="Reds",
            template=PLOTLY_TEMPLATE,
            projection="natural earth"
        )
        fig_map1.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
                landcolor="#e2e8f0",
                coastlinecolor="#cbd5e1",
                coastlinewidth=0.5
            ),
            font=dict(color="#0f172a")
        )
        st.plotly_chart(fig_map1, use_container_width=True)
    
    with col2:
        st.markdown("### 💉 Vaccination Rates")
        fig_map2 = px.choropleth(
            latest_global,
            locations="iso_code",
            color="vaccination_rate",
            hover_name="location",
            color_continuous_scale="Greens",
            template=PLOTLY_TEMPLATE,
            projection="natural earth"
        )
        fig_map2.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
                landcolor="#e2e8f0",
                coastlinecolor="#cbd5e1",
                coastlinewidth=0.5
            ),
            font=dict(color="#0f172a")
        )
        st.plotly_chart(fig_map2, use_container_width=True)
    
    # Continent Comparison
    st.markdown("### 🌍 Continent-wise Analysis")
    
    continent_summary = latest_global.groupby('continent').agg({
        'total_cases': 'sum',
        'total_deaths': 'sum',
        'population': 'sum',
        'vaccination_rate': 'mean'
    }).reset_index()
    
    continent_summary['cases_per_million'] = (continent_summary['total_cases'] / continent_summary['population']) * 1_000_000
    continent_summary['deaths_per_million'] = (continent_summary['total_deaths'] / continent_summary['population']) * 1_000_000
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig_cont = px.bar(
            continent_summary.sort_values('total_cases', ascending=False),
            x='continent',
            y='total_cases',
            title="Total Cases by Continent",
            color='total_cases',
            color_continuous_scale="Blues",
            template=PLOTLY_TEMPLATE
        )
        fig_cont.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_cont, use_container_width=True)
    
    with col4:
        fig_cont_vax = px.bar(
            continent_summary.sort_values('vaccination_rate', ascending=False),
            x='continent',
            y='vaccination_rate',
            title="Average Vaccination Rate by Continent",
            color='vaccination_rate',
            color_continuous_scale="Greens",
            template=PLOTLY_TEMPLATE
        )
        fig_cont_vax.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_cont_vax, use_container_width=True)
    
    # Scatter Geo
    st.markdown("### 📍 Geographic Scatter")
    # Note: This requires latitude/longitude data which may not be in the dataset
    # We'll create a simple bubble map instead
    
    fig_bubble = px.scatter_geo(
        latest_global.assign(total_cases=latest_global['total_cases'].fillna(0)),
        locations="iso_code",
        size="total_cases",
        hover_name="location",
        color="continent",
        size_max=50,
        template=PLOTLY_TEMPLATE,
        projection="natural earth"
    )
    fig_bubble.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(0,0,0,0)", landcolor="#e2e8f0")
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# =============================================================================
# VIEW 4: DEEP DIVE ANALYSIS
# =============================================================================
elif selected_tab == "🔬 Analysis":
    st.markdown("# 🔬 Deep Dive Analysis")
    st.markdown("Socio-economic correlations and multivariate insights")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scatter Plots
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 GDP vs Vaccination Rate")
        fig_scatter1 = px.scatter(
            latest_global,
            x="gdp_per_capita",
            y="vaccination_rate",
            size="population",
            color="continent",
            hover_name="location",
            log_x=True,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_scatter1.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_scatter1, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 HDI vs Mortality Rate")
        fig_scatter2 = px.scatter(
            latest_global,
            x="human_development_index",
            y="mortality_rate",
            size="population",
            color="continent",
            hover_name="location",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_scatter2.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_scatter2, use_container_width=True)
    
    # Correlation Heatmap
    st.markdown("### 🔥 Correlation Matrix")
    
    corr_cols = ['total_cases', 'total_deaths', 'gdp_per_capita', 'population_density', 
                'median_age', 'vaccination_rate', 'hospital_beds_per_thousand', 'life_expectancy']
    corr_df = latest_global[corr_cols] # Removed dropna to keep as much data as possible
    
    if not corr_df.empty and len(corr_df) > 10:
        corr_matrix = corr_df.corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="Spectral_r",
            template=PLOTLY_TEMPLATE,
            zmin=-1,
            zmax=1,
            labels=dict(color="Correlation")
        )
        fig_corr.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12, color="#0f172a"),
            xaxis=dict(tickfont=dict(color="#334155", size=11)),
            yaxis=dict(tickfont=dict(color="#334155", size=11)),
            coloraxis_colorbar=dict(
                title=dict(text="Correlation", font=dict(color="#0f172a")),
                tickfont=dict(color="#334155")
            )
        )
        fig_corr.update_traces(textfont=dict(size=11, color="#000000"))
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("Insufficient data for correlation analysis with current filters.")
    
    # NEW: Cases by Country Heatmap (Time Series)
    st.markdown("### 🌡️ Cases Heatmap - Top Countries Over Time")
    
    # Prepare data: monthly aggregation for readability
    heatmap_countries = global_df.groupby('location')['total_cases'].max().nlargest(15).index.tolist()
    heatmap_data = global_df[global_df['location'].isin(heatmap_countries)].copy()
    heatmap_data['month'] = heatmap_data['date'].dt.to_period('M').astype(str)
    
    heatmap_pivot = heatmap_data.groupby(['location', 'month'])['new_cases'].sum().reset_index()
    heatmap_matrix = heatmap_pivot.pivot(index='location', columns='month', values='new_cases').fillna(0)
    
    # Select every 3rd month for cleaner display
    if len(heatmap_matrix.columns) > 20:
        selected_months = heatmap_matrix.columns[::3]
        heatmap_matrix = heatmap_matrix[selected_months]
    
    fig_heatmap = px.imshow(
        heatmap_matrix,
        aspect="auto",
        color_continuous_scale="YlOrRd",
        title="Monthly New Cases Heatmap - Top 15 Countries",
        template=PLOTLY_TEMPLATE,
        labels=dict(x="Month", y="Country", color="New Cases")
    )
    fig_heatmap.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=45, tickfont=dict(color="#334155", size=9)),
        yaxis=dict(tickfont=dict(color="#334155", size=11)),
        coloraxis_colorbar=dict(
            title=dict(text="Cases", font=dict(color="#0f172a")),
            tickfont=dict(color="#334155")
        )
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    
    # Additional Scatter Plots
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 👥 Population Density vs Cases per Million")
        fig_scatter3 = px.scatter(
            latest_global,
            x="population_density",
            y="total_cases_per_million",
            size="population",
            color="continent",
            hover_name="location",
            log_x=True,
            template=PLOTLY_TEMPLATE
        )
        fig_scatter3.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter3, use_container_width=True)
    
    with col4:
        st.markdown("### 🏥 Hospital Beds vs Deaths per Million")
        fig_scatter4 = px.scatter(
            latest_global,
            x="hospital_beds_per_thousand",
            y="total_deaths_per_million",
            size="population",
            color="continent",
            hover_name="location",
            template=PLOTLY_TEMPLATE
        )
        fig_scatter4.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter4, use_container_width=True)

# =============================================================================
# VIEW 5: STATISTICAL ANALYSIS
# =============================================================================
elif selected_tab == "📉 Statistical":
    st.markdown("# 📉 Statistical Analysis")
    st.markdown("Distribution and statistical insights")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Cases Distribution")
        fig_hist1 = px.histogram(
            latest_global,
            x="total_cases_per_million",
            nbins=50,
            title="Distribution of Cases per Million",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS["cases"]]
        )
        fig_hist1.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hist1, use_container_width=True)
    
    with col2:
        st.markdown("### 💀 Mortality Rate Distribution")
        fig_hist2 = px.histogram(
            latest_global[latest_global['mortality_rate'] < 20],  # Filter outliers
            x="mortality_rate",
            nbins=40,
            title="Distribution of Mortality Rates",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS["danger"]]
        )
        fig_hist2.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hist2, use_container_width=True)
    
    # Box Plots
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 📦 Cases per Million by Continent")
        fig_box1 = px.box(
            latest_global,
            x="continent",
            y="total_cases_per_million",
            color="continent",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_box1.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_box1, use_container_width=True)
    
    with col4:
        st.markdown("### 🎻 Vaccination Rate Distribution")
        fig_violin = px.violin(
            latest_global,
            x="continent",
            y="vaccination_rate",
            color="continent",
            template=PLOTLY_TEMPLATE,
            box=True,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_violin.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_violin, use_container_width=True)
    
    # Summary Statistics
    st.markdown("### 📋 Summary Statistics")
    
    summary_stats = latest_global[['total_cases', 'total_deaths', 'vaccination_rate', 'mortality_rate']].describe()
    st.dataframe(summary_stats.style.background_gradient(cmap='viridis'), use_container_width=True)

# =============================================================================
# VIEW 6: ABOUT
# =============================================================================
elif selected_tab == "ℹ️ About":
    st.markdown("# ℹ️ About This Dashboard")
    
    st.markdown("""
    ## 🦠 COVID-19 Global Intelligence Dashboard
    
    ### Project Overview
    This high-end data visualization dashboard provides comprehensive analysis of the global COVID-19 pandemic,
    combining cutting-edge data science techniques with premium UI/UX design.
    
    ### 📊 Data Source
    - **Dataset**: Our World in Data (OWID) COVID-19 Dataset
    - **Coverage**: 237 countries from January 2020 to August 2024
    - **Update Frequency**: Daily
    - **Source**: [https://github.com/owid/covid-19-data](https://github.com/owid/covid-19-data)
    
    ### 🔧 Preprocessing Methodology
    
    The data undergoes rigorous preprocessing following industry best practices:
    
    1. **Data Cleaning**
       - Removal of aggregate entities (World, income groups, etc.)
       - Missing value imputation using forward-fill, interpolation, and median strategies
       - Outlier detection and handling
       - Data type conversions
    
    2. **Feature Engineering**
       - Vaccination rate calculations
       - Mortality rate (case fatality rate)
       - Active cases estimation
       - Per-population metrics
       - Growth rate indicators
    
    3. **Data Validation**
       - Negative value checks
       - Date range verification
       - Data consistency validation
    
    ### 📈 Visualizations
    
    This dashboard includes 15+ interactive visualizations:
    - Time series trends
    - Geographic choropleth maps
    - Correlation heatmaps
    - Distribution plots (histograms, box plots, violin plots)
    - Multivariate scatter plots
    - Comparative bar charts
    - Statistical summaries
    
    ### 💻 Technology Stack
    - **Frontend**: Streamlit
    - **Visualization**: Plotly, Seaborn, Matplotlib
    - **Data Processing**: Pandas, NumPy
    - **Design**: Custom CSS with dark theme and glassmorphism
    
    ### ⚠️ Limitations & Ethical Considerations
    
    - Data quality varies by country and reporting standards
    - Missing data for some countries/regions
    - Testing rates affect case counts
    - Definitions of "cases" and "deaths" may vary
    - Vaccination data may be incomplete for some regions
    
    ### 📝 License & Attribution
    
    This project is for educational and informational purposes.
    Data © Our World in Data - CC BY 4.0
    
    ### 👨‍💻 Developed By
    High-End Data Visualization Project
    """)
    
    st.markdown("---")
    st.markdown("**Last Updated**: December 2024")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; padding: 1rem;'>"
    "🦠 COVID-19 Global Intelligence Dashboard | Data © Our World in Data | "
    "Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)
