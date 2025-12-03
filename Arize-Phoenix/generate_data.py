import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range (Nov 2021 + some surrounding months)
start_date = datetime(2021, 10, 1)
end_date = datetime(2021, 12, 31)
dates = pd.date_range(start_date, end_date, freq='D')

# Define stores and products
stores = [1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329]
product_skus = [f"SKU_{i:04d}" for i in range(1, 51)]  # 50 different products

# Generate transactions
data = []
for date in dates:
    for store in stores:
        # Each store sells 5-15 different products per day
        n_products = np.random.randint(5, 16)
        selected_products = np.random.choice(product_skus, size=n_products, replace=False)
        
        for sku in selected_products:
            # Generate sales data
            base_price = np.random.uniform(10, 100)
            has_promotion = np.random.choice([0, 1], p=[0.7, 0.3])  # 30% chance of promotion
            
            if has_promotion:
                discount = np.random.uniform(0.1, 0.3)  # 10-30% discount
                price = base_price * (1 - discount)
                quantity = np.random.randint(10, 50)  # More sales during promotion
            else:
                price = base_price
                quantity = np.random.randint(5, 25)  # Regular sales
            
            sales_amount = price * quantity
            
            data.append({
                'store_id': store,
                'date': date.strftime('%Y-%m-%d'),
                'product_sku': sku,
                'quantity': quantity,
                'unit_price': round(price, 2),
                'sales_amount': round(sales_amount, 2),
                'promotion': has_promotion,
                'base_price': round(base_price, 2)
            })

# Create DataFrame
df = pd.DataFrame(data)

# Add some additional features for elasticity analysis
df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
df['month'] = pd.to_datetime(df['date']).dt.month

# Save to parquet
output_path = 'data/Store_Sales_Price_Elasticity_Promotions_Data.parquet'
df.to_parquet(output_path, index=False)

print(f"Generated {len(df)} records")
print(f"Saved to {output_path}")
print(f"\nData summary:")
print(df.head(10))
print(f"\nColumns: {list(df.columns)}")
print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
print(f"Stores: {sorted(df['store_id'].unique())}")
print(f"Products: {len(df['product_sku'].unique())}")
