import pandas as pd
import random
from datetime import datetime, timedelta

# Read the customer demand data
df = pd.read_csv('../data/customer_demand.csv')

def generate_delivery_document(order):
    # Randomly decide if this delivery will have discrepancies
    has_discrepancy = random.random() < 0.3  # 30% chance of discrepancy
    
    # Generate planned delivery date (1-3 days from order)
    order_date = datetime.now()
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

# Generate delivery documents for each customer and month
delivery_documents = []
for _, order in df.iterrows():
    delivery_doc = generate_delivery_document(order)
    delivery_documents.append(delivery_doc)

# Convert delivery documents to DataFrame
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
output_path = '../data/delivery_documents.csv'
delivery_df.to_csv(output_path, index=False)

print(f"Generated {len(delivery_documents)} delivery documents")
print(f"Saved to: {output_path}")