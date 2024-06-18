import pandas as pd

# Read the CSV file
df = pd.read_csv('all_needed_data.csv')

# Drop rows where WaitTime is NA
df = df.dropna(subset=['WaitTime'])

# Convert DateTimeOrderStart to datetime format
df['DateTimeOrderStart'] = pd.to_datetime(df['DateTimeOrderStart'])

# Filter rows where DateTimeOrderStart is not a Friday
df = df[df['DateTimeOrderStart'].dt.dayofweek == 4]  # 4 corresponds to Friday

# Extract date part from DateTimeOrderStart
df['Date'] = df['DateTimeOrderStart'].dt.date

# Group by date and count the number of orders for each day
orders_per_day = df.groupby('Date').size()

# Calculate the average number of orders per day
average_orders_per_day = orders_per_day.mean()

print("Average number of orders per day:", average_orders_per_day)
