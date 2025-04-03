#!/usr/bin/env python
"""
Main execution script for supply chain simulation.

This script provides a simple command-line interface to run
the supply chain simulation with different parameters.
"""

import pandas as pd
import argparse
import os
from io import StringIO

from config import PLANNING_LEAD_TIME
from product_generator import generate_apple_product_data, save_product_data
from data_utils import load_csv_data, load_from_string, save_csv_data
from simulation import run_supply_chain_simulation, save_simulation_results
from visualization import plot_shipping_routes_with_waypoints, save_and_display_map

def load_sample_data():
    """Load sample data for simulation from embedded strings.
    
    Returns:
        tuple: (harvest_data, demand_data) as DataFrames
    """
    # Sample harvest data
    harvest_csv = """SupplierID,Country,Apple Variety,Harvest Month,Harvest Quantity
S1,India,Royal Gala,August,600
S1,India,Royal Gala,September,600
S1,India,Fuji,August,200
S1,India,Fuji,September,200
S1,India,Fuji,October,200
S1,India,Golden Delicious,May,800
S1,India,Granny Smith,September,450
S1,India,Granny Smith,October,450
S1,India,Pink Lady,September,350
S1,India,Pink Lady,October,350
S2,South Africa,Royal Gala,January,864
S2,South Africa,Royal Gala,February,864
S2,South Africa,Royal Gala,March,864
S2,South Africa,Royal Gala,April,864
S2,South Africa,Royal Gala,May,864
S2,South Africa,Fuji,January,432
S2,South Africa,Fuji,February,432
S2,South Africa,Fuji,March,432
S2,South Africa,Fuji,April,432
S2,South Africa,Fuji,May,432
S2,South Africa,Golden Delicious,January,576
S2,South Africa,Golden Delicious,February,576
S2,South Africa,Golden Delicious,March,576
S2,South Africa,Golden Delicious,April,576
S2,South Africa,Golden Delicious,May,576
S2,South Africa,Granny Smith,January,648
S2,South Africa,Granny Smith,February,648
S2,South Africa,Granny Smith,March,648
S2,South Africa,Granny Smith,April,648
S2,South Africa,Granny Smith,May,648
S2,South Africa,Pink Lady,January,504
S2,South Africa,Pink Lady,February,504
S2,South Africa,Pink Lady,March,504
S2,South Africa,Pink Lady,April,504
S2,South Africa,Pink Lady,May,504
S3,Chile,Royal Gala,February,2640
S3,Chile,Royal Gala,March,2640
S3,Chile,Fuji,March,1320
S3,Chile,Fuji,April,1320
S3,Chile,Granny Smith,March,1980
S3,Chile,Granny Smith,April,1980
S3,Chile,Golden Delicious,February,1760
S3,Chile,Golden Delicious,March,1760
S3,Chile,Pink Lady,April,1540
S3,Chile,Pink Lady,May,1540
S4,New Zealand,Royal Gala,February,8400
S4,New Zealand,Fuji,March,2100
S4,New Zealand,Fuji,April,2100
S4,New Zealand,Granny Smith,April,3150
S4,New Zealand,Granny Smith,May,3150
S4,New Zealand,Golden Delicious,February,2800
S4,New Zealand,Golden Delicious,March,2800
S4,New Zealand,Pink Lady,April,2450
S4,New Zealand,Pink Lady,May,2450
"""

    # Sample demand data
    demand_csv = """city,customer_id,month,royal_gala,fuji,granny_smith,golden_delicious,pink_lady,total
Berlin,EDEKA,January,78,87,67,81,50,364
Berlin,EDEKA,February,73,81,64,76,49,343
Berlin,EDEKA,March,70,76,62,70,52,329
Berlin,EDEKA,April,67,70,56,64,53,311
Berlin,EDEKA,May,64,64,50,59,56,294
Berlin,EDEKA,June,59,56,48,53,50,266
Berlin,EDEKA,July,56,53,45,48,45,246
Berlin,EDEKA,August,76,62,48,53,42,280
Berlin,EDEKA,September,98,73,53,70,49,343
Berlin,EDEKA,October,106,90,64,81,57,399
Berlin,EDEKA,November,95,98,70,84,59,406
Berlin,EDEKA,December,90,92,73,87,57,399
Berlin,LIDL,January,70,78,60,73,45,325
Berlin,LIDL,February,65,73,58,68,44,306
Berlin,LIDL,March,63,68,55,63,46,294
Berlin,LIDL,April,60,63,50,58,48,278
Berlin,LIDL,May,58,58,45,53,50,263
Berlin,LIDL,June,53,50,43,48,45,238
Berlin,LIDL,July,50,48,40,43,40,220
Berlin,LIDL,August,68,55,43,48,38,250
Berlin,LIDL,September,88,65,48,63,44,306
Berlin,LIDL,October,95,80,58,73,51,356
Berlin,LIDL,November,85,88,63,75,53,363
Berlin,LIDL,December,80,83,65,78,51,356
Berlin,REWE,January,50,56,43,52,32,234
Berlin,REWE,February,47,52,41,49,32,221
Berlin,REWE,March,45,49,40,45,33,212
Berlin,REWE,April,43,45,36,41,34,200
Berlin,REWE,May,41,41,32,38,36,189
Berlin,REWE,June,38,36,31,34,32,171
Berlin,REWE,July,36,34,29,31,29,158
Berlin,REWE,August,49,40,31,34,27,180
Berlin,REWE,September,63,47,34,45,32,221
Berlin,REWE,October,68,58,41,52,37,257
Berlin,REWE,November,61,63,45,54,38,261
Berlin,REWE,December,58,59,47,56,37,257
Hamburg,EDEKA,January,42,48,36,45,27,198
Hamburg,EDEKA,February,39,45,35,42,26,186
Hamburg,EDEKA,March,38,42,33,39,29,180
Hamburg,EDEKA,April,36,39,30,36,29,170
Hamburg,EDEKA,May,35,36,27,33,30,161
Hamburg,EDEKA,June,32,30,26,30,27,144
Hamburg,EDEKA,July,30,29,24,27,24,134
Hamburg,EDEKA,August,42,33,26,30,23,153
Hamburg,EDEKA,September,54,39,29,39,26,186
Hamburg,EDEKA,October,57,48,35,45,32,216
Hamburg,EDEKA,November,51,54,38,47,32,221
Hamburg,EDEKA,December,48,51,39,48,30,216
Hamburg,LIDL,January,34,38,29,36,22,158
Hamburg,LIDL,February,31,36,28,34,20,149
Hamburg,LIDL,March,30,34,26,31,23,144
Hamburg,LIDL,April,29,31,24,29,23,136
Hamburg,LIDL,May,28,29,22,26,24,128
Hamburg,LIDL,June,25,24,20,24,22,115
Hamburg,LIDL,July,24,23,19,22,19,107
Hamburg,LIDL,August,34,26,20,24,18,122
Hamburg,LIDL,September,43,31,23,31,20,149
Hamburg,LIDL,October,46,38,28,36,25,173
Hamburg,LIDL,November,41,43,30,37,25,176
Hamburg,LIDL,December,38,41,31,38,24,173
Hamburg,REWE,January,24,27,20,26,15,112
Hamburg,REWE,February,22,26,20,24,14,105
Hamburg,REWE,March,21,24,19,22,16,102
Hamburg,REWE,April,20,22,17,20,16,96
Hamburg,REWE,May,20,20,15,19,17,91
Hamburg,REWE,June,18,17,14,17,15,82
Hamburg,REWE,July,17,16,14,15,14,76
Hamburg,REWE,August,24,19,14,17,13,87
Hamburg,REWE,September,31,22,16,22,14,105
Hamburg,REWE,October,32,27,20,26,18,122
Hamburg,REWE,November,29,31,21,26,18,125
Hamburg,REWE,December,27,29,22,27,17,122
Munich,EDEKA,January,34,40,29,37,23,164
Munich,EDEKA,February,33,37,28,34,22,153
Munich,EDEKA,March,31,34,26,33,23,147
Munich,EDEKA,April,29,31,25,29,25,140
Munich,EDEKA,May,28,29,22,26,26,132
Munich,EDEKA,June,26,25,20,25,23,119
Munich,EDEKA,July,25,23,19,22,22,110
Munich,EDEKA,August,34,28,20,25,20,127
Munich,EDEKA,September,43,33,23,33,22,153
Munich,EDEKA,October,48,40,28,37,26,180
Munich,EDEKA,November,43,45,31,39,28,186
Munich,EDEKA,December,40,42,33,40,26,181
Munich,LIDL,January,25,30,22,28,17,122
Munich,LIDL,February,24,28,21,25,16,114
Munich,LIDL,March,23,25,20,24,17,109
Munich,LIDL,April,22,23,18,22,18,104
Munich,LIDL,May,21,22,16,20,20,98
Munich,LIDL,June,20,18,15,18,17,89
Munich,LIDL,July,18,17,14,16,16,82
Munich,LIDL,August,25,21,15,18,15,94
Munich,LIDL,September,32,24,17,24,16,114
Munich,LIDL,October,36,30,21,28,20,133
Munich,LIDL,November,32,33,23,29,21,138
Munich,LIDL,December,30,31,24,30,20,135
Munich,REWE,January,22,26,19,24,15,106
Munich,REWE,February,21,24,18,22,14,99
Munich,REWE,March,20,22,17,21,15,95
Munich,REWE,April,19,20,16,19,16,90
Munich,REWE,May,18,19,14,17,17,85
Munich,REWE,June,17,16,13,16,15,77
Munich,REWE,July,16,15,12,14,14,71
Munich,REWE,August,22,18,13,16,13,82
Munich,REWE,September,28,21,15,21,14,99
Munich,REWE,October,31,26,18,24,17,116
Munich,REWE,November,28,29,20,25,18,120
Munich,REWE,December,26,27,21,26,17,117
"""
    
    df_harvest = load_from_string(harvest_csv)
    df_demand = load_from_string(demand_csv)
    
    return df_harvest, df_demand

def main():
    """Main function to run the simulation."""
    parser = argparse.ArgumentParser(description="Run apple supply chain simulation")
    
    parser.add_argument("--years", nargs="+", type=int, default=[2021],
                      help="Years to simulate (default: 2021)")
    
    parser.add_argument("--lead-time", type=int, default=PLANNING_LEAD_TIME,
                      help=f"Planning lead time in months (default: {PLANNING_LEAD_TIME})")
    
    parser.add_argument("--harvest-data", type=str,
                      help="Path to harvest data CSV file (optional)")
    
    parser.add_argument("--demand-data", type=str,
                      help="Path to demand data CSV file (optional)")
    
    parser.add_argument("--output", type=str, default="simulated_purchase_orders.csv",
                      help="Output filename for purchase orders (default: simulated_purchase_orders.csv)")
    
    parser.add_argument("--generate-products", action="store_true",
                      help="Generate product master data")
    
    parser.add_argument("--products-count", type=int, default=45,
                      help="Number of product records to generate (default: 45)")
    
    parser.add_argument("--map", action="store_true",
                      help="Generate shipping routes map")
    
    args = parser.parse_args()
    
    # Generate product data if requested
    if args.generate_products:
        print(f"Generating {args.products_count} product records...")
        product_data = generate_apple_product_data(args.products_count)
        save_product_data(product_data)
    
    # Load data
    if args.harvest_data and args.demand_data:
        print(f"Loading data from {args.harvest_data} and {args.demand_data}")
        df_harvest = load_csv_data(args.harvest_data)
        df_demand = load_csv_data(args.demand_data)
    else:
        print("Using sample data for simulation")
        df_harvest, df_demand = load_sample_data()
    
    if df_harvest is None or df_demand is None:
        print("Error loading required data. Exiting.")
        return
    
    # Run simulation
    print(f"Running simulation for years: {args.years} with lead time: {args.lead_time} months")
    po_df = run_supply_chain_simulation(
        df_harvest, 
        df_demand,
        simulation_years=args.years,
        planning_lead_time=args.lead_time
    )
    
    if po_df is not None and not po_df.empty:
        save_simulation_results(po_df, args.output)
    
    # Generate map if requested
    if args.map:
        print("Generating shipping routes map...")
        shipping_map = plot_shipping_routes_with_waypoints()
        save_and_display_map(shipping_map, "shipping_routes.html")

if __name__ == "__main__":
    main()