import pandas as pd
import matplotlib.pyplot as plt
import os
from math import log10
import matplotlib.patheffects as PathEffects
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Part 1: Data Processing

# Function to load data from the Excel file
def load_data(file_path):
    input_data = pd.read_excel(file_path)
    input_data.dropna(how='all', inplace=True)  # Remove rows with all NaN values
    return input_data

# Function to process the data according to the task requirements
def process_data(input_data, cluster_colors):
    # Keep only the required columns
    output_data = input_data[['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count']]
    
    # Add the color column based on the cluster_colors dictionary
    output_data['color'] = output_data['cluster'].map(cluster_colors)
    
    # Remove duplicates of words in the same area
    output_data = output_data.drop_duplicates(subset=['area', 'keyword'])
    
    # Rename the columns as specified
    output_data.columns = ['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count', 'color']
    
    return output_data

# Function to check if the number of keywords in input and output data match
def check_keywords_number(input_data, output_data):
    number_of_keyword = input_data['keyword'].nunique()
    if(number_of_keyword - output_data['keyword'].nunique() != 0):
        print('В ходе выполнения задания был нарушен пункт 5')

# Function to sort the output data according to the task requirements
def sort_output_data(output_data):
    return output_data.sort_values(['area', 'cluster', 'cluster_name', 'count'],
                                      ascending=[True, True, True, False])

# Function to save the output data to a Google Spreadsheet
def save_output_data(output_data, credentials_file, sheet_id):
    output_data = output_data.fillna('')
    output_data.to_csv('output_data.csv')
    
    # Authenticate with Google Sheets API using a service account
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    sheets_instance = build('sheets', 'v4', credentials=credentials)
    
    # Update the Google Sheet with the output data
    sheets_instance.spreadsheets().values().update(
        spreadsheetId=sheet_id, range='Sheet1', 
        body={'values': [output_data.columns.tolist()] + output_data.values.tolist()},
        valueInputOption='RAW'
    ).execute()

# Part 2: Plotting

# Function to split long phrases into multiple lines
def split_long_phrases(s, max_len=15):
    if len(s) > max_len:
        split_index = s[:max_len].rfind(' ')
        if split_index == -1:
            split_index = max_len
        return s[:split_index] + '\n' + split_long_phrases(s[split_index:].strip(), max_len)
    return s

# Function to scale font size based on the count
def size_scaler(x, max_count):
    return 10 * log10(x / pow(max_count, 1/2) + 10) + 2

# Function to create scatter plots for each area
def create_scatter_plots(output_data, cluster_colors):
    areas = output_data['area'].unique()
    
    # Create a directory to save the scatter plot mages
    if not os.path.exists('scatter_plots'):
        os.makedirs('scatter_plots')
    # Iterate through each area to create a scatter plot
    for area in areas:
        area_data = output_data[output_data['area'] == area].copy()
        area_data['count'] = pd.to_numeric(area_data['count'], errors='coerce')
        area_data['count'].fillna(1, inplace=True)
        max_count = area_data['count'].max()

        fig, ax = plt.subplots(figsize=(15, 15))
        
        # Plot each point and add text labels
        for index, row in area_data.iterrows():
            ax.scatter(row['x'], row['y'], s=1.4 * row['count'], c=row['color'], edgecolors='k', alpha=0.7)
            text = ax.text(row['x'], row['y'], split_long_phrases(row['keyword']), 
                        fontsize=size_scaler(row['count'], max_count), ha='center', va='center', fontname='Arial')
            text.set_path_effects([PathEffects.withStroke(linewidth=3,foreground='w')])
        
        # Set plot title and axis labels
        ax.set_title(f'Scatter plot for area {area}', fontname='Arial')
        ax.set_xlabel('x', fontname='Arial')
        ax.set_ylabel('y', fontname='Arial')
        
        # Add legend for clusters
        for cluster, color in cluster_colors.items():
            cluster_name = area_data[area_data['cluster'] == cluster]['cluster_name'].iloc[0]
            ax.scatter([], [], c=color, label=f'{cluster_name} ({cluster})', edgecolors='k', alpha=0.7)
        ax.legend(title='Clusters', prop={'family': 'Arial'})

        # Save the scatter plot image as a PNG file
        plt.savefig(f'scatter_plots/scatter_plot_area_{area}.png', dpi=100)
        plt.close(fig)

#Main function to execute the data processing and plotting tasks
def main():
    input_file_path = 'Тестовое задание.xlsx'
    credentials_file = 'your_credentials.json'
    sheet_id = '1mHADS6i7cD5ZEHIBeSXZo9B26fIJlJ3VBDVH1ffuaM4'
    # Define a dictionary to map cluster numbers to colors
    cluster_colors = {
        0: '#ff7f0e',
        1: '#2ca02c',
        2: '#d62728',
        3: '#9467bd',
    }

    # Load, process, and save the data
    input_data = load_data(input_file_path)
    output_data = process_data(input_data, cluster_colors)
    check_keywords_number(input_data, output_data)
    output_data = sort_output_data(output_data)
    save_output_data(output_data, credentials_file, sheet_id)

    # Create scatter plots
    create_scatter_plots(output_data, cluster_colors)

#Call the main function to start the execution
main()