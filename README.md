# COVID-19 & Public Response Visualization Analysis

This project analyzes COVID-19 spread, vaccination rates, and public response using a data cleaning pipeline and an interactive Streamlit dashboard.

## Project Structure
- `data_preprocessing.ipynb`: Jupyter Notebook containing the code for loading, cleaning, and preprocessing the raw data.
- `app.py`: Streamlit application file for visualizing the data.
- `owid-covid-data.csv`: Source data file (from Our World in Data).
- `cleaned_covid_data.csv`: Output of the preprocessing step, used by the dashboard.

## Setup Instructions

1.  **Environment Setup**:
    Ensure you have Python installed. Install the required libraries:
    ```bash
    pip install pandas numpy streamlit plotly
    ```

2.  **Data Cleaning**:
    To generate the clean dataset required for the app, you can run the logic provided in `data_preprocessing.ipynb`. A `cleaned_covid_data.csv` file must exist in the directory.

3.  **Running the App**:
    Execute the following command in your terminal to launch the dashboard:
    ```bash
    python -m streamlit run app.py
    ```
    Alternatively, you can simply double-click the `run_app.bat` file I created for you.

## Analysis Process using Best Practices

1.  **Handling Missing Data**:
    - Aggregated daily stats (new cases/deaths) were filled with 0 where missing.
    - Cumulative stats (total cases, people vaccinated) were forward-filled to maintain the last known record.
    - Non-country entities were removed to prevent data duplication and skew.

2.  **Feature Engineering**:
    - `vaccination_rate` was calculated as `(people_vaccinated / population) * 100` to allow for fair comparison between countries of different sizes.

## Visualizations
The dashboard includes:
- **Time Series Line Charts**: Compare trends in cases, deaths, or vaccinations for multiple countries.
- **Global Heatmap**: Visualize the geographic distribution of any metric on a specific date.
- **Multivariate Scatter Plot**: Explore the relationship between vaccination rates and case counts, with bubble size representing population.



python -m streamlit run app.py