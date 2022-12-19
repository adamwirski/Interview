import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(url):
    # Create an URL object
    # Create object page
    page = requests.get(url)
    # print(page)

    # parser-lxml = Change html to Python friendly format
    # Obtain page's information
    soup = BeautifulSoup(page.text, 'lxml')

    # Obtain information from tag <table>
    table1 = soup.find(text="Abilene, Texas").find_parent("table")
    # table1 = soup.find('table', id='anyid')

    # print(table1)

    # Obtain every title of columns with tag <th>
    headers = ['Name', 'Latitude', 'Longitude', 'Elevation']


    # print(headers)

    # Create a dataframe
    mydata = pd.DataFrame(columns = headers)

    # Create a for loop to fill mydata
    for j in table1.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(mydata)
        mydata.loc[length] = row
    # print(mydata)
    mydata.drop(mydata.index[0], inplace=True)
    mydata.reset_index(inplace=True, drop=True)

    # Cleaning and modeling data to expected result
    cleaned_data = mydata[['Name', 'Latitude', 'Longitude']]
    cleaned_data = cleaned_data[cleaned_data['Name'].str.contains('Ho|Ta')]
    for x in cleaned_data.index:
        Latitude = str(cleaned_data.loc[x, "Latitude"])
        Longitude = str(cleaned_data.loc[x, "Longitude"])

        # adding period to location data
        Latitude = Latitude[:3] +'.' + Latitude[3:]
        Longitude = Longitude[:3] +'.' + Longitude[3:]

        # removing the side indicator
        Latitude = Latitude[:-1]
        Longitude = Longitude[:-1]

        # removing white spaces
        Latitude = Latitude.replace(" ", "")
        Longitude= Longitude.replace(" ", "")

        # removing the zero if the coordinates are below 100
        if Latitude[0] == '0':
            Latitude = Latitude[1:]
        if Longitude[0] == '0':
            Longitude = Longitude[1:]

        #     assign the values back after trensforming them
        cleaned_data.loc[x, "Latitude"] = (Latitude)
        cleaned_data.loc[x, "Longitude"] = (Longitude)
    # Export to csv
    cleaned_data.to_csv('web_scrapping/capital_cities.csv', index=False)
#
# def clean_before_loading(df):
#     # df.astype({'Name': 'object'}).dtypes
#     # df.astype({'Date': 'datetime64'}).dtypes
#     # df.astype({'Latitude': 'float64'}).dtypes
#     # df.astype({'Longitude': 'float64'}).dtypes
#     # # df.astype({'Name': 'string'}).dtypes
#     # print(df.dtypes)
#     return df