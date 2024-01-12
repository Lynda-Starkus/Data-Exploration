import os
import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from folium.plugins import MarkerCluster
from fastdtw import fastdtw
from scipy.stats import pearsonr
import seaborn as sns

# Specify the folder where your files are stored
folder_path = 'data/vehicles_preprocessed'

# Get a list of all parquet files in the specified folder
parquet_files = [f for f in os.listdir(folder_path) if f.endswith('.parquet')]
print('parquet files',parquet_files)
# Create an empty DataFrame to hold the combined data
combined_df = pd.DataFrame()

# Loop through each file, read the data, and concatenate it to the combined DataFrame
for file in parquet_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_parquet(file_path, engine='fastparquet')
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Clean and organize the data
combined_df['t'] = pd.to_datetime(combined_df['t'])
combined_df['hour'] = combined_df['t'].dt.hour
combined_df['day_of_week'] = combined_df['t'].dt.day_name()



combined_df['mode'] = combined_df['mode'].apply(lambda x: x[0])
combined_df['nb_usagers'] = combined_df['nb_usagers'].apply(lambda x: x[0])



# Replace missing values with appropriate values or strategies
combined_df['mode'].fillna('Unknown', inplace=True)
combined_df['nb_usagers'].fillna(0, inplace=True)

print(combined_df)
# Convert 'nb_usagers' to numeric
combined_df['nb_usagers'] = pd.to_numeric(combined_df['nb_usagers'], errors='coerce')

# Drop NaN values in specific columns
combined_df.dropna(subset=['latitude', 'longitude'], inplace=True)

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

print(combined_df['nb_usagers'])
# Generate detailed advanced EDA with interactive plots
# Example 1: Interactively plot the nb_usagers of different vehicle types over time
plt.figure(figsize=(15, 8))
combined_df['mode_str'] = combined_df['mode'].astype(str)
sns.lineplot(x='t', y='nb_usagers', hue='mode_str', data=combined_df.sort_values('t'))
plt.title('Interactive Plot: Vehicle Type nb_usagers Over Time')
plt.xlabel('Time')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.legend(title='Vehicle Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# Example 2: Interactively plot a heatmap of vehicle nb_usagerss using plotly
fig = px.density_heatmap(combined_df, x='longitude', y='latitude', nbinsx=20, nbinsy=20, marginal_x="histogram", marginal_y="histogram",
                         title='Interactive Heatmap: Vehicle Density',
                         labels={'latitude': 'Latitude', 'longitude': 'Longitude'},
                         hover_data={'latitude': True, 'longitude': True, 'nb_usagers': True})
fig.show()

# Example 3: Visualize data on a map using Folium with clustering
map_center = [combined_df['latitude'].mean(), combined_df['longitude'].mean()]
mymap = folium.Map(location=map_center, zoom_start=14)

# Drop NaN values in latitude and longitude before creating the map
combined_df.dropna(subset=['latitude', 'longitude'], inplace=True)

# Cluster the data for better visualization
kmeans = KMeans(n_clusters=5, random_state=42).fit(combined_df[['latitude', 'longitude']])
combined_df['cluster'] = kmeans.labels_

marker_cluster = MarkerCluster().add_to(mymap)

# Add markers for each cluster
for cluster in combined_df['cluster'].unique():
    cluster_data = combined_df[combined_df['cluster'] == cluster]
    for index, row in cluster_data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=f"{row['label']}, {row['t']}", icon=folium.Icon(color='blue')).add_to(marker_cluster)

# Save the map to an HTML file
mymap.save('vehicle_map_clusters.html')

# Display descriptive statistics and information about the DataFrame
print(combined_df.describe())
print(combined_df.info())

# Plot histograms for selected variables
plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
sns.histplot(combined_df['nb_usagers'], kde=True, bins=30, color='skyblue')
plt.title('Histogram: Vehicle nb_usagerss')

plt.subplot(2, 2, 2)
sns.histplot(combined_df['hour'], kde=True, bins=24, color='salmon')
plt.title('Histogram: Hourly Distribution')

plt.subplot(2, 2, 3)
sns.histplot(combined_df['latitude'], kde=True, bins=30, color='green')
plt.title('Histogram: Latitude Distribution')

plt.subplot(2, 2, 4)
sns.histplot(combined_df['longitude'], kde=True, bins=30, color='orange')
plt.title('Histogram: Longitude Distribution')

plt.tight_layout()
plt.show()

# Plot correlation matrix
plt.figure(figsize=(10, 8))
correlation_matrix = combined_df[['nb_usagers', 'hour', 'latitude', 'longitude']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix')
plt.show()

# Extract time series for each segment and plot all series in one graphic
segments = combined_df['label'].unique()

plt.figure(figsize=(15, 8))
for segment in segments:
    segment_data = combined_df[combined_df['label'] == segment]
    plt.plot(segment_data['t'], segment_data['nb_usagers'], label=segment)

plt.title('Vehicle nb_usagerss Time Series for Each Segment')
plt.xlabel('Time')
plt.ylabel('nb_usagers')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.show()

# Calculate DTW and Pearson correlation between different segments
for i in range(len(segments)):
    for j in range(i + 1, len(segments)):
        segment_i = combined_df[combined_df['label'] == segments[i]]['nb_usagers']
        segment_j = combined_df[combined_df['label'] == segments[j]]['nb_usagers']

        # Check if the segments have more than one data point and equal lengths
        if len(segment_i) > 1 and len(segment_j) > 1 and len(segment_i) == len(segment_j):
            # Calculate DTW
            distance, path = fastdtw(segment_i, segment_j)

            # Calculate Pearson correlation
            pearson_corr, _ = pearsonr(segment_i, segment_j)

            print(f"DTW between {segments[i]} and {segments[j]}: {distance}")
            print(f"Pearson correlation between {segments[i]} and {segments[j]}: {pearson_corr}")
            print()
        else:
            print(f"Segments {segments[i]} or {segments[j]} have insufficient or unequal data points for DTW calculation.")

