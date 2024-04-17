import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the data
df = pd.read_csv('wNumOpen.csv')

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
df_filtered = df.dropna(subset=['WaitTime'])

# Drop rows where WaitTime is NA
df_filtered = df.dropna(subset=['WaitTime'])

# Convert columns to numeric if necessary
df_filtered['NumOpenTickets'] = pd.to_numeric(df_filtered['NumOpenTickets'], errors='coerce')
df_filtered['WaitTime'] = pd.to_numeric(df_filtered['WaitTime'], errors='coerce')

# Sample 2% of the data randomly
df_sampled = df_filtered.sample(frac=0.02, random_state=42)

# Plot the dot plot
plt.figure(figsize=(10, 6))
plt.scatter(df_sampled['NumOpenTickets'], df_sampled['WaitTime'], alpha=0.5)
plt.xlabel('Number of Open Tickets')
plt.ylabel('Wait Time (minutes)')
plt.grid(True)

# Calculate and plot the line of best fit
coefficients = np.polyfit(df_sampled['NumOpenTickets'], df_sampled['WaitTime'], 1)
poly = np.poly1d(coefficients)
plt.plot(df_sampled['NumOpenTickets'], poly(df_sampled['NumOpenTickets']), color='red')

# Calculate R-squared
residuals = df_sampled['WaitTime'] - poly(df_sampled['NumOpenTickets'])
ss_res = np.sum(residuals**2)
ss_tot = np.sum((df_sampled['WaitTime'] - np.mean(df_sampled['WaitTime']))**2)
r_squared = 1 - (ss_res / ss_tot)

plt.legend()
plt.show()

print(f'R-squared = {r_squared:.2f}. That means {r_squared:.2f}% of the variability in the dependent variable is explained by the independent variable.')
