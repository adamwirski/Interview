from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def push_csv_to_gsheet(csv_path, sheet_id, creds):
    API = build('sheets', 'v4', credentials=creds)
    with open(csv_path, 'r') as csv_file:
        csvContents = csv_file.read()
    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": 0,
                    "rowIndex": "0",  # adapt this if you need different positioning
                    "columnIndex": "0", # adapt this if you need different positioning
                },
                "data": csvContents,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }
    request = API.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=body)
    response = request.execute()
    return response


# # upload
# with open(path_to_credentials, 'rb') as token:
#     credentials = pickle.load(token)
#
# API = build('sheets', 'v4', credentials=credentials)
#
# push_csv_to_gsheet(
#     csv_path=path_to_csv,
#     sheet_id=find_sheet_id_by_name(worksheet_name)
# )