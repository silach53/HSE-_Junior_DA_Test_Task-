# Part 2: Plotting
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import pandas as pd
import os


cluster_colors = {
    0: 'violet',
    1: 'red',
    2: 'green',
    3: 'blue',
}

# Define a function to split long phrases
def split_long_phrases(s, max_len=15):
    if len(s) > max_len:
        split_index = s[:max_len].rfind(' ')
        if split_index == -1:
            split_index = max_len
        return s[:split_index] + '\n' + split_long_phrases(s[split_index:].strip(), max_len)
    return s

output_data = pd.read_csv('output_data')

# Create scatter plots for each area
areas = output_data['area'].unique()

if not os.path.exists('scatter_plots'):
    os.makedirs('scatter_plots')

for area in areas:
    area_data = output_data[output_data['area'] == area]
    area_data['count'] = pd.to_numeric(area_data['count'], errors='coerce') # Convert 'count' column to numeric data type, non-numeric values to NaN
    area_data['count'].fillna(1, inplace=True) # Replace NaN values with a default value (e.g., 1)
    max_count = area_data['count'].max()

    fig, ax = plt.subplots(figsize=(15, 15))
    for index, row in area_data.iterrows():
        ax.scatter(row['x'], row['y'], s=row['count'], c=row['color'], edgecolors='k', alpha=0.7)
        text = ax.text(row['x'], row['y'], split_long_phrases(row['keyword']), fontsize=row['count']*28/max_count, ha='center', va='center', fontname='Arial')
        text.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='w')])

    ax.set_title(f'Scatter plot for area {area}', fontname='Arial')
    ax.set_xlabel('x', fontname='Arial')
    ax.set_ylabel('y', fontname='Arial')

    # Create a legend for clusters
    for cluster, color in cluster_colors.items():
        cluster_name = area_data[area_data['cluster'] == cluster]['cluster_name'].iloc[0]
        ax.scatter([], [], c=color, label=f'{cluster_name} ({cluster})', edgecolors='k', alpha=0.7)
    ax.legend(title='Clusters', prop={'family': 'Arial'})

    plt.savefig(f'scatter_plots/scatter_plot_area_{area}.png', dpi=100)
    plt.close(fig)