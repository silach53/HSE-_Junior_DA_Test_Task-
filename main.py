import pandas as pd
import matplotlib.pyplot as plt
import os
from math import log10

# Part 1: Data Processing

# Load the data from the source
# Replace 'Тестовое задание.xlsx' with the path to your input data
input_data = pd.read_excel('Тестовое задание.xlsx')

number_of_keyword = input_data['keyword'].nunique()

input_data.dropna(how='all', inplace=True)

# Keep the required columns
output_data = input_data[['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count']]

# Assign colors to phrases based on cluster
cluster_colors = {
    0: 'violet',
    1: 'red',
    2: 'green',
    3: 'blue',
}

output_data['color'] = output_data['cluster'].map(cluster_colors)

# Remove duplicates of keywords in the same area
output_data = output_data.drop_duplicates(subset=['area', 'keyword'])

# Rename columns if needed
output_data.columns = ['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count', 'color']

if(number_of_keyword-output_data['keyword'].nunique() != 0):
    print('В ходе выполнения задания был нарушен пункт 5') 
    # Количество переданных в исходных ключевых слов должно совпадать с количество слов в выходных данных 
    #(за исключением дублированных строк или строк с пустыми\неформатными значениями по ключевым показателям 
    #[перечислены в п. 1], если такие имеются).

# Sort the output data
output_data = output_data.sort_values(['area', 'cluster', 'cluster_name', 'count'],
                                      ascending=[True, True, True, False])


output_data.to_csv('output_data.csv')
# Save the output data to a Google Spreadsheet (make sure to have Google API credentials set up)
# or you can save it as a csv file using output_data.to_csv('output_data.csv', index=False)
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file('your_credentials.json')
sheet_id = '1mHADS6i7cD5ZEHIBeSXZo9B26fIJlJ3VBDVH1ffuaM4'

output_data = output_data.fillna('')
sheets_instance = build('sheets', 'v4', credentials=credentials)
sheets_instance.spreadsheets().values().update(
    spreadsheetId=sheet_id, range='Sheet1', body={'values': [output_data.columns.tolist()] + output_data.values.tolist()},
    valueInputOption='RAW'
).execute()

max_count = max(pd.to_numeric(output_data['count'], errors='coerce'))

# Part 2: Plotting
import matplotlib.patheffects as PathEffects

# Define a function to split long phrases
def split_long_phrases(s, max_len=15):
    if len(s) > max_len:
        split_index = s[:max_len].rfind(' ')
        if split_index == -1:
            split_index = max_len
        return s[:split_index] + '\n' + split_long_phrases(s[split_index:].strip(), max_len)
    return s

# Create scatter plots for each area
areas = output_data['area'].unique()

if not os.path.exists('scatter_plots'):
    os.makedirs('scatter_plots')

mas = []

def size_scaler(x,max_count):
    print(x,max_count)
    f = 10*log10(x/pow(max_count,1/2)+10)
    mas.append(f)
    return f

for area in areas:
    area_data = output_data[output_data['area'] == area]
    area_data['count'] = pd.to_numeric(area_data['count'], errors='coerce') # Convert 'count' column to numeric data type, non-numeric values to NaN
    area_data['count'].fillna(1, inplace=True) # Replace NaN values with a default value (e.g., 1)
    max_count = area_data['count'].max()

    fig, ax = plt.subplots(figsize=(15, 15))
    for index, row in area_data.iterrows():
        ax.scatter(row['x'], row['y'], s=1.4*row['count'], c=row['color'], edgecolors='k', alpha=0.7)
        
        text = ax.text(row['x'], row['y'], split_long_phrases(row['keyword']), fontsize=size_scaler(row['count'],max_count),
                        ha='center', va='center', fontname='Arial')
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

print([round(x) for x in mas])