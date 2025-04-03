# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Supply chain simulation for apple varieties using Python and pandas for synthetic data generation. The project simulates the journey of apples from suppliers in multiple countries to supermarkets in Germany.

## Environment & Run Commands
- Run Jupyter notebooks: `jupyter notebook src/scm_data_gen.ipynb`
- Install dependencies: `pip install pandas folium geopy`
- Add new visualizations: `import folium` and `from IPython.display import display`
- Save CSV output: `df.to_csv("data/filename.csv", index=False)`

## Code Style Guidelines
- Follow PEP 8 for Python code formatting
- Use docstrings for functions with Args/Returns sections:
  ```python
  def generate_apple_product_data(num_records=100):
      """
      Generates synthetic data for an apple product table.

      Args:
          num_records (int): The number of records to generate.

      Returns:
          pandas.DataFrame: A DataFrame containing the synthetic data.
      """
  ```
- Name variables descriptively with snake_case: `harvest_by_supplier`, `shipping_routes`
- Include comments for complex data transformations:
  ```python
  # Convert month names to numbers for easier comparison
  df_harvest['HarvestMonthNum'] = df_harvest['Harvest Month'].map(month_map)
  ```
- Keep functions focused on single responsibilities
- Use pandas for data manipulation: `monthly_demand = df_demand_melted.groupby(['MonthNum', 'Apple Variety'])['DemandQuantity'].sum().reset_index()`
- Map lookups preferred over repetitive conditionals:
  ```python
  month_map = {'January': 1, 'February': 2, ...}
  df_harvest['HarvestMonthNum'] = df_harvest['Harvest Month'].map(month_map)
  ```
- Handle errors with try/except when processing geographic data:
  ```python
  try:
      po_df.to_csv(output_filename, index=False)
      print(f"Purchase order results saved to: {os.path.abspath(output_filename)}")
  except Exception as e:
      print(f"Error saving purchase orders to CSV: {e}")
  ```

## Data Management
- Store CSV files in the data/ directory: `data/harvest_by_supplier.csv`, `data/products.csv`
- Include headers in all CSV files: 'SupplierID', 'Country', 'Apple Variety', etc.
- Document data sources in markdown files like `apple_harvest_varities.md`
- Use consistent date formatting (YYYY-MM-DD): `2021-01-26`
- For simulation data, use descriptive filenames: `simulated_purchase_orders_2021.csv`