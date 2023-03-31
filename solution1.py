import pandas as pd

# Load the data from the source
# Replace 'input_data.csv' with the path to your input data
input_data = pd.read_excel('Тестовое задание.xlsx')

number_of_keyword = input_data['keyword'].nunique()

input_data.dropna(how='all',inplace=True)
#После этого шага в таблице 228 строк, так как существовала полностью пустая строка в excel

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
#После этого шага в таблице 221 строчка

# Rename columns if needed
output_data.columns = ['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count', 'color']

if(number_of_keyword-output_data['keyword'].nunique() != 0):
    print('В ходе выполнения задания был нарушен пункт 5') 
    # Количество переданных в исходных ключевых слов должно совпадать с количество слов в выходных данных 
    #(за исключением дублированных строк или строк с пустыми\неформатными значениями по ключевым показателям 
    #[перечислены в п. 1], если такие имеются).

# Sort the output data
#Сортировка должна происходить по колонкам area, cluster, cluster_name, count 
#(по count значения сортируются в убывающем порядке, в остальных - по возрастающему).
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