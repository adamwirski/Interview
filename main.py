#
#
#
# take the google sheet and put into pandas
#
# for every record check sunset etc and update dataframe
#
# import data to big query if doesnt exist
from google_sheets import authenticate

# authenticate app to make changes to google sheets
auth = authenticate.main('credentials/google_sheet_oath.json')

