import pandas as pd
import matplotlib.pyplot as plt
import os
from math import log10
import matplotlib.patheffects as PathEffects
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Part 1: Data Processing

def load_data(file_path):
    input_data = pd.read_excel(file_path)
    input_data.dropna(how='all', inplace=True)
    return input_data

def process_data(input_data,cluster_colors):
    output_data = input_data[['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count']]
    output_data['color'] = output_data['cluster'].map(cluster_colors)
    output_data = output_data.drop_duplicates(subset=['area', 'keyword'])
    output_data.columns = ['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count', 'color']
    return output_data

def check_keywords_number(input_data, output_data):
    number_of_keyword = input_data['keyword'].nunique()
    if(number_of_keyword - output_data['keyword'].nunique() != 0):
        print('В ходе выполнения задания был нарушен пункт 5')

def sort_output_data(output_data):
    return output_data.sort_values(['area', 'cluster', 'cluster_name', 'count'],
                                      ascending=[True, True, True, False])

def save_output_data(output_data, credentials_file, sheet_id):
    output_data = output_data.fillna('')
    output_data.to_csv('output_data.csv')
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    sheets_instance = build('sheets', 'v4', credentials=credentials)
    sheets_instance.spreadsheets().values().update(
        spreadsheetId=sheet_id, range='Sheet1', 
        body={'values': [output_data.columns.tolist()] + output_data.values.tolist()},
        valueInputOption='RAW'
    ).execute()

# Part 2: Plotting

def split_long_phrases(s, max_len=15):
    if len(s) > max_len:
        split_index = s[:max_len].rfind(' ')
        if split_index == -1:
            split_index = max_len
        return s[:split_index] + '\n' + split_long_phrases(s[split_index:].strip(), max_len)
    return s

def size_scaler(x, max_count):
    return 10 * log10(x / pow(max_count, 1/2) + 10)

def create_scatter_plots(output_data,cluster_colors):
    areas = output_data['area'].unique()
    if not os.path.exists('scatter_plots'):
        os.makedirs('scatter_plots')

    for area in areas:
        area_data = output_data[output_data['area'] == area].copy()
        area_data['count'] = pd.to_numeric(area_data['count'], errors='coerce')
        area_data['count'].fillna(1, inplace=True)
        max_count = area_data['count'].max()

        fig, ax = plt.subplots(figsize=(15, 15))
        for index, row in area_data.iterrows():
            ax.scatter(row['x'], row['y'], s=1.4 * row['count'], c=row['color'], edgecolors='k', alpha=0.7)
            text = ax.text(row['x'], row['y'], split_long_phrases(row['keyword']), 
                           fontsize=size_scaler(row['count'], max_count), ha='center', va='center', fontname='Arial')
            text.set_path_effects([PathEffects.withStroke(linewidth=3,foreground='w')])
        ax.set_title(f'Scatter plot for area {area}', fontname='Arial')
        ax.set_xlabel('x', fontname='Arial')
        ax.set_ylabel('y', fontname='Arial')
        
        for cluster, color in cluster_colors.items():
            cluster_name = area_data[area_data['cluster'] == cluster]['cluster_name'].iloc[0]
            ax.scatter([], [], c=color, label=f'{cluster_name} ({cluster})', edgecolors='k', alpha=0.7)
        ax.legend(title='Clusters', prop={'family': 'Arial'})

        plt.savefig(f'scatter_plots/scatter_plot_area_{area}.png', dpi=100)
        plt.close(fig)

def main():
    input_file_path = 'Тестовое задание.xlsx'
    credentials_file = 'your_credentials.json'
    sheet_id = '1mHADS6i7cD5ZEHIBeSXZo9B26fIJlJ3VBDVH1ffuaM4'

    cluster_colors = {
        0: '#ff7f0e',
        1: '#2ca02c',
        2: '#d62728',
        3: '#9467bd',
    }

    input_data = load_data(input_file_path)
    output_data = process_data(input_data,cluster_colors)
    check_keywords_number(input_data, output_data)
    output_data = sort_output_data(output_data)
    save_output_data(output_data, credentials_file, sheet_id)
    create_scatter_plots(output_data,cluster_colors)

main()