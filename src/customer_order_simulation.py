import pandas as pd
import random
from datetime import datetime, timedelta

# Read the customer demand data
df = pd.read_csv('../data/customer_demand.csv')

def generate_delivery_document(order, current_date):
    # Randomly decide if this delivery will have discrepancies
    has_discrepancy = random.random() < 0.3  # 30% chance of discrepancy
    
    # Generate planned delivery date (1-3 days from order)
    order_date = current_date
    planned_delivery = order_date + timedelta(days=random.randint(1, 3))
    
    # If there's a discrepancy, delay delivery by 1-5 days
    actual_delivery = planned_delivery
    if has_discrepancy:
        actual_delivery = planned_delivery + timedelta(days=random.randint(1, 5))
    
    # Create delivery quantities (potentially with shortages)
    delivery = {}
    apple_types = ['royal_gala', 'fuji', 'granny_smith', 'golden_delicious', 'pink_lady']
    
    for apple in apple_types:
        ordered_qty = order[f'{apple}(metrictons)']
        if has_discrepancy:
            # Deliver 70-95% of ordered quantity
            delivery[apple] = round(ordered_qty * random.uniform(0.7, 0.95), 1)
        else:
            delivery[apple] = ordered_qty
            
    return {
        'order_number': random.randint(10000, 99999),
        'customer_id': order['customer_id'],
        'city': order['city'],
        'order_date': order_date.strftime('%Y-%m-%d'),
        'planned_delivery_date': planned_delivery.strftime('%Y-%m-%d'),
        'actual_delivery_date': actual_delivery.strftime('%Y-%m-%d'),
        'ordered_quantities': {apple: order[f'{apple}(metrictons)'] for apple in apple_types},
        'delivered_quantities': delivery,
        'has_discrepancy': has_discrepancy
    }

# Generate delivery documents for each customer and month across multiple years
delivery_documents = []
month_mapping = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

# Generate for 2023, 2024, and April 2025
years = [2023, 2024]
for year in years:
    for _, order in df.iterrows():
        month = month_mapping[order['month']]
        current_date = datetime(year, month, random.randint(1, 28))
        delivery_doc = generate_delivery_document(order, current_date)
        delivery_documents.append(delivery_doc)

# Generate for April 2025
april_2025_data = df[df['month'] == 'April']
for _, order in april_2025_data.iterrows():
    current_date = datetime(2025, 4, random.randint(1, 28))
    delivery_doc = generate_delivery_document(order, current_date)
    delivery_documents.append(delivery_doc)

# Convert to DataFrame
def convert_to_dataframe(delivery_documents):
    rows = []
    for doc in delivery_documents:
        row = {
            'order_number': doc['order_number'],
            'customer_id': doc['customer_id'],
            'city': doc['city'],
            'order_date': doc['order_date'],
            'planned_delivery_date': doc['planned_delivery_date'],
            'actual_delivery_date': doc['actual_delivery_date'],
            'has_discrepancy': doc['has_discrepancy']
        }
        
        # Add ordered quantities columns
        for apple, qty in doc['ordered_quantities'].items():
            row[f'ordered_{apple}'] = qty
            
        # Add delivered quantities columns
        for apple, qty in doc['delivered_quantities'].items():
            row[f'delivered_{apple}'] = qty
            
        rows.append(row)
    
    return pd.DataFrame(rows)

# Convert to DataFrame and save as CSV
delivery_df = convert_to_dataframe(delivery_documents)
# Sort by order date
delivery_df['order_date'] = pd.to_datetime(delivery_df['order_date'])
delivery_df = delivery_df.sort_values('order_date')
output_path = '../data/customer_delivery_documents.csv'
delivery_df.to_csv(output_path, index=False)

print(f"Generated {len(delivery_documents)} delivery documents")
print(f"Date range: 2023-01-01 to 2025-04-30")
print(f"Saved to: {output_path}")