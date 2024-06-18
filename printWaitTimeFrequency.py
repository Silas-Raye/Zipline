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

# Drop rows with missing values in the 'WaitTime' column
df = df.dropna(subset=['WaitTime'])

# Round up every wait time to the nearest 5-minute increment
df['RoundedWaitTime'] = np.ceil(df['WaitTime'] / 5) * 5

# Count the frequency of each rounded wait time
rounded_wait_time_counts = df['RoundedWaitTime'].value_counts().sort_index()

# Plotting the bar chart
min_year = df['DateTimeOrderStart'].dt.year.min()
max_year = df['DateTimeOrderStart'].dt.year.max()
rounded_wait_time_counts.plot(kind='bar')
plt.xlabel('Wait Time (in Minutes)')
plt.ylabel(f'Number of Orders (from {min_year} to {max_year})')
plt.gca().set_yticklabels(['{:.0f}K'.format(x/1000) for x in plt.gca().get_yticks()]) # Divide y-axis labels by 1000
plt.show()
