# gspread02.py

import gspread
from google.oauth2.service_account import Credentials

scope = ['https://www.googleapis.com/auth/spreadsheets']


# Use the JSON key file for authentication
creds = Credentials.from_service_account_file('./haranggotgam-22ece62e15d4.json', scopes=scope)
# scopes=['https://www.googleapis.com/auth/spreadsheets'])

client = gspread.authorize(creds)

# Open the sheet by its ID
# key = location, it's in the google sheets link
# if link is https://docs.google.com/spreadsheets/d/1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8/edit#gid=1609248418
# key is 1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8
sheet = client.open_by_key("1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8").sheet1

cell_range = sheet.range('A1:H10') 
cell_list = sheet.get('A1:N11')[10]
print(cell_list)