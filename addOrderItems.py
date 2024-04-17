import pandas as pd
import numpy as np

# Load the CSV files into pandas DataFrames
wNumOpen_df = pd.read_csv("wNumOpen.csv")
orderItem_df = pd.read_csv("SatchelsDB/orderItem.csv")

# Select only the required columns from orderItem.csv
orderItem_df = orderItem_df[['OrderId', 'MenuItemId', 'Count']]

# Group by OrderId and aggregate MenuItemId and Count into a dictionary
orderItem_grouped = orderItem_df.groupby('OrderId').apply(lambda x: dict(zip(x['MenuItemId'], x['Count']))).reset_index()

# Rename the columns for clarity
orderItem_grouped.columns = ['OrderId', 'OrderItems']

# Merge the two DataFrames on OrderId
merged_df = pd.merge(wNumOpen_df, orderItem_grouped, on='OrderId', how='left')

# Fill NaN values with an empty dictionary
merged_df['OrderItems'] = merged_df['OrderItems'].fillna({})

# Step 1: Create isWeekend column
merged_df['DateTimeOrderStart'] = pd.to_datetime(merged_df['DateTimeOrderStart'])
merged_df['isWeekend'] = merged_df['DateTimeOrderStart'].dt.dayofweek.isin([4, 5])

# Define a function to extract quantities for each menu item type
def extract_quantity(order_items_dict, item_id):
    if isinstance(order_items_dict, float) and np.isnan(order_items_dict):
        return 0
    elif item_id in order_items_dict:
        return order_items_dict[item_id]
    else:
        return 0

# Create new columns for each menu item type and extract quantities
merged_df['NumSilces'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 1))
merged_df['NumMed'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 2))
merged_df['NumLrg'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 3))
merged_df['NumPanSlice'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 4))
merged_df['NumPan'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 5))
merged_df['NumMFP'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 7))
merged_df['NumIndy'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 8))
merged_df['NumZone'] = merged_df['OrderItems'].apply(lambda x: extract_quantity(x, 9))

# To save the merged DataFrame to a CSV file
merged_df.to_csv("all_needed_data.csv", index=False)
