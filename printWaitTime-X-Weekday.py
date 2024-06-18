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

# Drop rows where WaitTime is NA
df_filtered = df.dropna(subset=['WaitTime'])

# Convert columns to numeric if necessary
df_filtered['WaitTime'] = pd.to_numeric(df_filtered['WaitTime'], errors='coerce')

# Convert DateTimeOrderStart column to datetime if it's not already
df['DateTimeOrderStart'] = pd.to_datetime(df['DateTimeOrderStart'])

# Extract day of the week from DateTimeOrderStart
df['DayOfWeek'] = df['DateTimeOrderStart'].dt.day_name()

# Filter out Sunday and Monday
filtered_df = df[~df['DayOfWeek'].isin(['Sunday', 'Monday'])]

# Reorder the DayOfWeek column
day_order = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
filtered_df['DayOfWeek'] = pd.Categorical(filtered_df['DayOfWeek'], categories=day_order, ordered=True)

# Plotting the box plot
plt.figure(figsize=(10, 6))  # Set the figure size
boxplot = filtered_df.boxplot(column='WaitTime', by='DayOfWeek', patch_artist=True)
plt.xlabel('Day of the Week')
plt.ylabel('Wait Time')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()
