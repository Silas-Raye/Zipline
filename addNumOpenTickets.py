import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Import the data
df = pd.read_csv('SatchelsOrders.csv')

# Clean up the data
df['PickupTime'] = df['PickupTime'].replace('9999-12-31 23:59:59.9999999', pd.NA)
df['DateTimeOrderStart'] = pd.to_datetime(df['DateTimeOrderStart'])
df['DateTimeLastOrderItemSent'] = pd.to_datetime(df['DateTimeLastOrderItemSent'])
df['DateTimeOrderPaid'] = pd.to_datetime(df['DateTimeOrderPaid'])
if df['PickupTime'] is not pd.NA:
    df['PickupTime'] = pd.to_datetime(df['PickupTime'], errors='coerce')
    df['PickupTime'] = df['PickupTime'].dt.floor('s')  # Floor to seconds, removing milliseconds
df['WaitTime'] = pd.NA
mask = df['DateTimeOrderStart'].dt.date == df['PickupTime'].dt.date
df.loc[mask, 'WaitTime'] = round((df['PickupTime'] - df['DateTimeOrderStart']).dt.total_seconds() / 60)
df.loc[(df['WaitTime'] < 0) | (df['WaitTime'] > 120), 'WaitTime'] = pd.NA

# Grouping the DataFrame by the 'DateTimeOrderStart' column
grouped = df.groupby(df['DateTimeOrderStart'].dt.date)

# Initialize an empty list to store the number of open tickets for each row
num_open_tickets_list = []

# Iterate over each group (day) using tqdm for a progress bar
for date, group_df in tqdm(grouped, desc="Processing Days", total=len(grouped)):
    # Iterate over each row in the group
    for idx, row in group_df.iterrows():
        # Filter earlier tickets based on conditions
        earlier_tickets = group_df[(group_df['DateTimeOrderStart'] < row['DateTimeOrderStart']) & 
                                    (group_df['DateTimeOrderPaid'] > row['DateTimeOrderStart'])]
        # Append the number of open tickets to the list
        num_open_tickets_list.append(len(earlier_tickets))

# Add the NumOpenTickets column to the original dataframe
df['NumOpenTickets'] = num_open_tickets_list

# Export
df.to_csv('output.csv', index=False)
