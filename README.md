# 🦠 COVID-19 Global Intelligence Dashboard

**A High-End Data Visualization Project**

> Professional-grade data visualization showcasing a self-contained Jupyter notebook with complete preprocessing pipeline and an interactive premium dashboard.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.17+-purple.svg)](https://plotly.com/)

---

## 📋 Project Overview

This project provides comprehensive COVID-19 pandemic analysis through:

- **Self-Contained Jupyter Notebook**: Complete analysis from raw data to insights (53 cells, 16 visualizations)
- **Premium Interactive Dashboard**: 6 analytical views with modern dark theme
- **Industry-Standard Methods**: Rigorous preprocessing, feature engineering, validation

**Dataset Coverage**: 237 countries | January 2020 - August 2024 | 395,000+ records

---

## 📁 Project Structure

```
COVID-19 Project/
│
├── 📓 project_notebook.ipynb     # COMPLETE notebook (preprocessing + 16 vizs)
├── 🎯 app.py                      # Premium Streamlit dashboard
│
├── 📄 owid-covid-data.csv         # Raw dataset (OWID)
├── ✅ cleaned_covid_data.csv      # Processed data (auto-generated)
│
├── 📋 requirements.txt            # Dependencies
├── 📖 README.md                   # This file
└── 📝 description.txt             # Project requirements
```

**Just 2 Main Files**: Everything you need is in `project_notebook.ipynb` and `app.py`!

---

## ✨ Features

### Jupyter Notebook (Self-Contained)
✅ **Complete Preprocessing Pipeline** (no external scripts!)
- Remove aggregate entities
- Advanced missing value imputation (4 strategies)
- Feature engineering (6 new metrics)
- Data validation

✅ **16 Professional Visualizations**
- Time series analysis
- Choropleth maps
- Scatter plots (GDP vs vaccination, HDI vs mortality)
- Correlation heatmap
- Distribution plots (box, violin, histogram)
- Hierarchical views (sunburst, treemap)

✅ **Comprehensive Documentation**
- Markdown explanations for every step
- Key insights and conclusions
- Data quality assessment
- Ethical considerations

### Interactive Dashboard
✅ **6 Analytical Views**
- Executive Overview
- Trends & Evolution
- Geographic Analysis
- Deep Dive Analysis
- Statistical Analysis
- About & Methodology

✅ **Premium Design**
- Modern dark theme with glassmorphism
- Vibrant color palettes (Turbo, Plasma, Viridis)
- Smooth animations and hover effects
- Responsive layout

✅ **Smart Interactivity**
- Date range filters
- Continent/country selectors
- Multiple metric options
- Log scale toggling

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Option A: Run Jupyter Notebook** (Complete Analysis)
   ```bash
   jupyter notebook project_notebook.ipynb
   ```
   
   The notebook does EVERYTHING:
   - Loads raw data (`owid-covid-data.csv`)
   - Performs all preprocessing
   - Creates 16 visualizations
   - Generates `cleaned_covid_data.csv`

3. **Option B: Run Dashboard** (After notebook or if data exists)
   ```bash
   python -m streamlit run app.py
   ```
   
   Opens at `http://localhost:8501`

---

## 📊 What's in the Notebook?

### Complete Table of Contents

1. **Environment Setup** - Import libraries
2. **Data Loading** - Load raw COVID-19 dataset
3. **Data Preprocessing Pipeline** (5 steps)
   - Remove aggregates
   - Handle missing values
   - Engineer features
   - Validate data
   - Export cleaned data
4. **Data Quality Assessment** - Report statistics
5. **16 Visualizations**
   - Global pandemic timeline
   - Top 20 countries (bar chart)
   - Choropleth maps (cases, vaccinations)
   - Multi-country trends
   - Vaccination progress
   - Box plots by continent
   - Mortality distribution
   - GDP vs vaccination scatter
   - HDI vs mortality scatter
   - Correlation heatmap
   - Population density analysis
   - Violin plots
   - Cumulative deaths (area chart)
   - Sunburst hierarchy
   - Treemap
6. **Insights & Conclusions** - Key findings

**All in ONE notebook** - No external scripts needed!

---

## 📈 Data Processing Highlights

### Missing Value Handling
- **Cumulative metrics**: Forward-fill by country
- **Daily increments**: Fill with 0
- **Smoothed metrics**: Linear interpolation
- **Per capita**: Backward + forward fill

### Feature Engineering
Six new calculated metrics:
- `vaccination_rate` = (vaccinated / population) × 100
- `fully_vaccinated_rate`
- `mortality_rate` (case fatality rate)
- `active_cases`
- `cases_per_population`
- `deaths_per_population`

### Results
- Original: 429,435 rows
- Cleaned: 395,311 rows
- Countries: 237
- 78% reduction in missing values for key metrics

---

## 🎨 Visualization Highlights

All visualizations feature:
- 🎨 Dark themes with vibrant colors
- 🔍 Interactive zoom, pan, hover
- 📱 Responsive layouts
- ✨ Professional styling
- 💫 Smooth animations

**Types Used**:
Line charts | Bar charts | Choropleth maps | Scatter plots | Box plots | Violin plots | Histograms | Heatmaps | Area charts | Sunburst | Treemap

---

## 🛠️ Technology Stack

**Data Processing**: Pandas, NumPy  
**Visualization**: Plotly, Seaborn, Matplotlib  
**Dashboard**: Streamlit, streamlit-extras  
**Environment**: Jupyter Notebook  

---

## 📚 Data Source

**Our World in Data - COVID-19 Dataset**
- Source: https://github.com/owid/covid-19-data
- License: Creative Commons BY 4.0
- Citation: Mathieu, E., et al. (2020). Coronavirus Pandemic (COVID-19). Our World in Data.

---

## 📝 Usage Notes

### For Grading/Presentation

1. **Start with the Notebook**: It's self-contained and shows the complete pipeline
2. **Then the Dashboard**: Interactive exploration of the same data
3. **Everything's Included**: No external scripts, just run and view!

### For Development

Both files are independent:
- **Notebook**: Can regenerate cleaned data from scratch
- **Dashboard**: Uses pre-cleaned data for speed

---

## ⚖️ Ethical Considerations

- Per capita metrics for fair comparisons
- Data quality limitations acknowledged
- Testing bias considerations noted
- Privacy protection (aggregated data only)
- Transparent visualization methods

---

## 📞 Support

**Key Files**:
- `project_notebook.ipynb` - Complete analysis (START HERE)
- `app.py` - Interactive dashboard
- `requirements.txt` - All dependencies

**Tips**:
- Notebook cells are executable in order
- Dashboard auto-caches for performance
- All visualizations use dark themes

---

<div align="center">

**✨ High-End Data Visualization Project ✨**

Made with ❤️ using Python, Plotly, and Streamlit

**Semester 5 - Fall 2025**

</div>