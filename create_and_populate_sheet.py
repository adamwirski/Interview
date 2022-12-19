# main executable file to run the whole program
import datetime
from time import sleep

import pandas
from google.oauth2 import service_account

import connect_to_sunrise_api
import load_to_bigquery
from web_scrapping import scrape_and_clean_locations
from google_sheets import authenticate
from google_sheets import create_new_sheet
from google_sheets import update_sheet_values
from google_sheets import read_sheet

from tqdm import tqdm

# authenticate app to make changes to google sheets
# auth = authenticate.main('credentials/google_sheet_oath.json')
credentials = service_account.Credentials.from_service_account_file("C:\\Users\\adamw\\IdeaProjects\\Interview\\credentials\\adam_service_account.json")

# create google sheet
sheet_id = create_new_sheet.create('test3', credentials)

# scrape locations data from website
scrape_and_clean_locations.scrape_table('http://euro.ecom.cmu.edu/program/courses/tcr854/2002/Software/20_854/html/cities.html')

# upload data to previously created google sheet
update_sheet_values.push_csv_to_gsheet('web_scrapping/capital_cities.csv', sheet_id, credentials)

# read from previously pushed google spreadsheet and sava data into a pandas dataframe
# normally this and above line would be run in different programs, but for the case of this excercise, I'll put them both here to present my knowledge

df = pandas.DataFrame(read_sheet.get_values(sheet_id, 'A:Z', credentials)['values'])
df = df.iloc[1: , :]
df.columns = ['Name', 'Latitude', 'Longitude']
header_list = ['Name', 'Date', 'Latitude', 'Longitude', 'TIME_OF_DAWN', 'TIME_OF_DUSK', 'TIME_OF_SUNRISE', 'TIME_OF_SUNSET']
df = df.reindex(columns = header_list)
df = df.reset_index()  # make sure indexes pair with number of rows
df = df[['Name', 'Date', 'Latitude', 'Longitude', 'TIME_OF_DAWN', 'TIME_OF_DUSK', 'TIME_OF_SUNRISE', 'TIME_OF_SUNSET']]

# print(df)
df_length = len(df)
start_date = datetime.date.today()
rows = df.iterrows()
print('Starting filling locations data from sunset API: ')
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    if index > 0:
        for single_date in (start_date - datetime.timedelta(n) for n in range(3)):
            try:
                api_data = connect_to_sunrise_api.get_data(row['Latitude'], row['Longitude'], single_date)

                # making break between API calls due to tandard API restrictions made by most cloud security services.
                # usuall api call delay should be around 1 sec, but as it's not a LIVE program, we should be fine making it smaller
                # sleep(0.1)

                df.loc[len(df.index)] = [
                    row['Name'],
                    single_date,
                    row['Latitude'],
                    row['Longitude'],
                    datetime.datetime.strptime(api_data['dawn'], '%I:%M:%S %p'),
                    datetime.datetime.strptime(api_data['dusk'], '%I:%M:%S %p'),
                    datetime.datetime.strptime(api_data['sunrise'], '%I:%M:%S %p'),
                    datetime.datetime.strptime(api_data['sunset'], '%I:%M:%S %p'),
                ]
            except:
                print('error fetching API data for: ', row['Name'])
                df.loc[len(df.index)] = [
                    row['Name'],
                    single_date,
                    row['Latitude'],
                    row['Longitude'],
                    None,
                    None,
                    None,
                    None
                ]
df = df.iloc[df_length:,:]
df.reset_index
print('Finished requesting sunset API data')

# # prepare data for loading with correct datatypes
# scrape_and_clean_locations.clean_before_loading(df)


load_to_bigquery.load(df)
