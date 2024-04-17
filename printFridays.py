import pandas as pd

# Read the CSV file
df = pd.read_csv('all_needed_data.csv')

# Drop rows where WaitTime is NA
df = df.dropna(subset=['WaitTime'])

# Convert DateTimeOrderStart to datetime format
df['DateTimeOrderStart'] = pd.to_datetime(df['DateTimeOrderStart'])

# Filter rows where DateTimeOrderStart is not a Friday
# df = df[df['DateTimeOrderStart'].dt.dayofweek == 5]  # 4 corresponds to Friday
df = df[df['DateTimeOrderStart'].dt.dayofweek.isin([1, 2, 3])]

# Define the rush hour time range
rush_hour_start = pd.to_datetime('17:00:00').time()
rush_hour_end = pd.to_datetime('21:00:00').time()

# Define a function to check if a datetime is within rush hour
def is_rush_hour(datetime):
    time = datetime.time()
    return rush_hour_start <= time <= rush_hour_end

# Apply the function to create the 'IsRushHr' column
df['IsRushHr'] = df['DateTimeOrderStart'].apply(is_rush_hour)

# Reset index after filtering
df = df.reset_index(drop=True)

# Save the modified dataframe to a new CSV file
df.to_csv('weekday_data.csv', index=False)
