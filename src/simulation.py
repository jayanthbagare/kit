"""
Supply chain simulation module.

This module contains the core simulation logic for the apple supply chain.
"""

import pandas as pd
import random
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

from config import INV_MONTH_MAP, MONTH_MAP, VARIETY_MAP, COUNTRY_PORT_MAP, PLANNING_LEAD_TIME, get_output_path
from data_utils import validate_dataframe, save_csv_data, load_from_string

def prepare_harvest_data(df_harvest):
    """Prepare harvest data for simulation.
    
    Args:
        df_harvest (pandas.DataFrame): Raw harvest data
        
    Returns:
        pandas.DataFrame: Processed harvest data
    """
    # Validate input
    required_columns = ['SupplierID', 'Country', 'Apple Variety', 'Harvest Month', 'Harvest Quantity']
    if not validate_dataframe(df_harvest, required_columns, "Harvest data"):
        return None
    
    # Add numeric month column
    df_harvest['HarvestMonthNum'] = df_harvest['Harvest Month'].map(MONTH_MAP)
    
    # Map shipping times to countries
    df_shipping = load_shipping_data()
    if df_shipping is not None:
        shipping_dict = df_shipping.set_index('Origin Port')['Average Shipping Time (Days)'].to_dict()
        df_harvest['ShippingDays'] = df_harvest['Country'].map(COUNTRY_PORT_MAP).map(shipping_dict)
    
    return df_harvest

def prepare_demand_data(df_demand):
    """Prepare demand data for simulation.
    
    Args:
        df_demand (pandas.DataFrame): Raw demand data
        
    Returns:
        pandas.DataFrame: Processed demand data and demand dictionary
    """
    # Validate input
    required_columns = ['month', 'royal_gala', 'fuji', 'granny_smith', 'golden_delicious', 'pink_lady']
    if not validate_dataframe(df_demand, required_columns, "Demand data"):
        return None, None
    
    # Add numeric month column
    df_demand['MonthNum'] = df_demand['month'].map(MONTH_MAP)
    
    # Melt demand data for easier aggregation
    df_demand_melted = df_demand.melt(
        id_vars=['city', 'customer_id', 'month', 'MonthNum'],
        value_vars=['royal_gala', 'fuji', 'granny_smith', 'golden_delicious', 'pink_lady'],
        var_name='Apple Variety',
        value_name='DemandQuantity'
    )
    
    # Map apple variety names to match harvest data format
    df_demand_melted['Apple Variety'] = df_demand_melted['Apple Variety'].map(VARIETY_MAP)
    
    # Calculate total demand per variety per month
    monthly_demand = df_demand_melted.groupby(['MonthNum', 'Apple Variety'])['DemandQuantity'].sum().reset_index()
    # Convert to dictionary for quick lookup: {(MonthNum, Variety): Quantity}
    demand_dict = monthly_demand.set_index(['MonthNum', 'Apple Variety'])['DemandQuantity'].to_dict()
    
    return df_demand_melted, demand_dict

def load_shipping_data():
    """Load and prepare shipping data.
    
    Returns:
        pandas.DataFrame: Processed shipping data
    """
    # Sample shipping data (hardcoded for now, could be loaded from a file)
    shipping_csv = """Origin Port,Destination Port,Approximate Distance (km),Average Energy Consumption (kWh),Average Cost (EUR),Average Shipping Time (Days)
    Jawaharlal Nehru Port Sheva Navi Mumbai,Albert Plesmanweg 240 Rotterdam,21700,325.5,534,30
    Port of Cape Town,Albert Plesmanweg 240 Rotterdam,11100,166.5,250,25
    Port of San Antonio,Albert Plesmanweg 240 Rotterdam,13900,208.5,702,26
    Ports of Auckland,Albert Plesmanweg 240 Rotterdam,17600,264.0,860,58"""
    
    return load_from_string(shipping_csv)

def create_available_supply_pool(df_harvest, simulation_years):
    """Create available supply pool for the simulation.
    
    Args:
        df_harvest (pandas.DataFrame): Processed harvest data
        simulation_years (list): List of years to simulate
        
    Returns:
        pandas.DataFrame: Available harvest data with quantities
    """
    # Validate input
    if df_harvest is None:
        return None
    
    available_harvest_list = []
    
    for year in simulation_years:
        df_year_harvest = df_harvest.copy()
        df_year_harvest['Year'] = year
        df_year_harvest['AvailableQuantity'] = df_year_harvest['Harvest Quantity']
        # Create a unique harvest identifier
        df_year_harvest['HarvestID'] = df_year_harvest.apply(
            lambda row: f"{row['SupplierID']}_{row['Apple Variety']}_{row['HarvestMonthNum']}_{row['Year']}", axis=1
        )
        available_harvest_list.append(df_year_harvest)

    available_harvest = pd.concat(available_harvest_list, ignore_index=True)
    available_harvest = available_harvest.set_index('HarvestID', drop=False)  # Set index for easy lookup and update
    
    return available_harvest

def run_supply_chain_simulation(df_harvest, df_demand, simulation_years=[2021], planning_lead_time=None):
    """Run the supply chain simulation.
    
    Args:
        df_harvest (pandas.DataFrame): Raw harvest data
        df_demand (pandas.DataFrame): Raw demand data
        simulation_years (list): List of years to simulate
        planning_lead_time (int, optional): Planning lead time in months, defaults to config value
        
    Returns:
        pandas.DataFrame: Generated purchase orders
    """
    # Use default planning lead time if not specified
    planning_lead_time = planning_lead_time or PLANNING_LEAD_TIME
    
    # Prepare data
    df_harvest_processed = prepare_harvest_data(df_harvest)
    if df_harvest_processed is None:
        return None
        
    df_demand_melted, demand_dict = prepare_demand_data(df_demand)
    if df_demand_melted is None or demand_dict is None:
        return None
    
    # Create available supply pool
    available_harvest = create_available_supply_pool(df_harvest_processed, simulation_years)
    if available_harvest is None:
        return None
    
    # Initialize simulation variables
    purchase_orders = []
    po_counter = 1
    
    print(f"Starting PO Simulation for {simulation_years[0]}-{simulation_years[-1]}...")
    print(f"Planning Lead Time: {planning_lead_time} months")
    print("-" * 30)

    # Simulate month by month
    for year in simulation_years:
        for sim_month in range(1, 13):
            sim_date = datetime(year, sim_month, 1)
            target_demand_date = sim_date + relativedelta(months=planning_lead_time)
            target_month = target_demand_date.month
            target_year = target_demand_date.year

            print(f"--- Simulating Month: {sim_date.strftime('%Y-%m')} ---")
            print(f"Planning for Demand Month: {target_demand_date.strftime('%Y-%m')}")

            # Get demand for the target month
            target_demands = {
                variety: qty for (m, variety), qty
                in demand_dict.items() if m == target_month
            }

            if not target_demands:
                # This handles cases where target month goes beyond Dec (e.g., planning in Nov/Dec 2024 for 2025)
                # Or if demand data is missing for a future month we calculate.
                print(f"No demand data found or required for target month {target_demand_date.strftime('%Y-%m')}. Skipping.")
                continue

            for variety, needed_qty in target_demands.items():
                if needed_qty <= 0: 
                    continue

                fulfilled_qty = 0
                print(f"  Target Demand for {variety}: {needed_qty}")

                # Find potential supply: Harvested *before or during* sim_month, correct variety, quantity > 0
                potential_supply = available_harvest[
                    (available_harvest['Apple Variety'] == variety) &
                    (available_harvest['AvailableQuantity'] > 0) &
                    # Harvest must have happened by the simulation date
                    ( (available_harvest['Year'] < year) | 
                      ((available_harvest['Year'] == year) & 
                       (available_harvest['HarvestMonthNum'] <= sim_month)) )
                ].copy()  # Copy to avoid SettingWithCopyWarning

                # Sort by harvest date: most recent first (fresher)
                potential_supply = potential_supply.sort_values(
                    by=['Year', 'HarvestMonthNum'], 
                    ascending=[False, False]
                )

                if potential_supply.empty:
                    print(f"    WARNING: No available supply found for {variety} harvested by "
                          f"{sim_date.strftime('%Y-%m')} to meet demand for "
                          f"{target_demand_date.strftime('%Y-%m')}")
                    continue

                # Process each potential supply source until demand is met
                _create_purchase_orders(
                    potential_supply, 
                    needed_qty, 
                    fulfilled_qty, 
                    variety,
                    available_harvest, 
                    sim_date, 
                    target_demand_date,
                    purchase_orders, 
                    po_counter
                )

                # Update PO counter
                po_counter += len(potential_supply)
                
                # Check if demand was fully met
                final_fulfilled = sum([po['QuantityOrdered'] for po in purchase_orders 
                                    if po['AppleVariety'] == variety and 
                                       po['DemandMonthTarget'] == target_demand_date.strftime('%Y-%m')])
                                       
                if final_fulfilled < needed_qty:
                    print(f"    WARNING: Could not fully meet demand for {variety} for "
                          f"{target_demand_date.strftime('%Y-%m')}. Shortfall: "
                          f"{needed_qty - final_fulfilled:.0f} units.")

    # Create DataFrame from purchase orders
    po_df = pd.DataFrame(purchase_orders)

    print("\n" + "=" * 30)
    print("Simulation Complete.")
    print(f"Total Purchase Orders Generated: {len(po_df)}")
    print("=" * 30 + "\n")

    # Display sample purchase orders
    if not po_df.empty:
        print("Sample Purchase Orders Generated:")
        print(po_df.head().to_string())
        print("...")
        print(po_df.tail().to_string())
    else:
        print("No purchase orders were generated.")
        
    return po_df

def _create_purchase_orders(potential_supply, needed_qty, fulfilled_qty, variety,
                           available_harvest, sim_date, target_demand_date,
                           purchase_orders, po_counter):
    """Helper function to create purchase orders from potential supply.
    
    Args:
        potential_supply (pandas.DataFrame): Potential supply sources
        needed_qty (float): Quantity needed to fulfill demand
        fulfilled_qty (float): Quantity already fulfilled
        variety (str): Apple variety being ordered
        available_harvest (pandas.DataFrame): Available harvest data
        sim_date (datetime): Current simulation date
        target_demand_date (datetime): Target demand date
        purchase_orders (list): List to append purchase orders to
        po_counter (int): Purchase order counter
        
    Returns:
        None: Updates purchase_orders list in place
    """
    for idx, (harvest_id, supply_row) in enumerate(potential_supply.iterrows()):
        if fulfilled_qty >= needed_qty:
            break  # Demand for this variety is met

        order_qty = min(needed_qty - fulfilled_qty, supply_row['AvailableQuantity'])

        if order_qty > 0:
            # Place the order
            supplier_id = supply_row['SupplierID']
            country = supply_row['Country']
            shipping_days = supply_row['ShippingDays']
            # Use timedelta for reliable date addition with days
            expected_arrival_date = sim_date + pd.Timedelta(days=int(shipping_days))

            po_record = {
                'PO_ID': f"PO_{po_counter + idx:05d}",
                'OrderDate': sim_date.strftime('%Y-%m-%d'),
                'SupplierID': supplier_id,
                'Country': country,
                'AppleVariety': variety,
                'QuantityOrdered': order_qty,
                'HarvestMonth': INV_MONTH_MAP[supply_row['HarvestMonthNum']],
                'HarvestYear': supply_row['Year'],
                'ExpectedArrivalDate': expected_arrival_date.strftime('%Y-%m-%d'),
                'DemandMonthTarget': target_demand_date.strftime('%Y-%m'),
                'SourceHarvestID': harvest_id
            }
            purchase_orders.append(po_record)

            # Update available quantity
            available_harvest.loc[harvest_id, 'AvailableQuantity'] -= order_qty
            fulfilled_qty += order_qty

            print(f"    Placed PO {po_record['PO_ID']}: {order_qty:.0f} units of {variety} "
                  f"from {supplier_id} ({country}) - Harvested {po_record['HarvestMonth']}/"
                  f"{po_record['HarvestYear']}. Arrival ~{po_record['ExpectedArrivalDate']}")

def save_simulation_results(po_df, filename="simulated_purchase_orders.csv"):
    """Save simulation results to a CSV file.
    
    Args:
        po_df (pandas.DataFrame): Purchase order data
        filename (str): Name of the output file
        
    Returns:
        bool: True if saving was successful, False otherwise
    """
    if po_df is None or po_df.empty:
        print("No purchase orders to save.")
        return False
        
    output_path = get_output_path(filename)
    return save_csv_data(po_df, output_path, "Error saving purchase orders")
