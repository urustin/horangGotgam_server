import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope
scope = ['https://docs.google.com/spreadsheets/d/1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8/edit#gid=1609248418']

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("./jsonKeyfile/haranggotgam-22ece62e15d4.json", scope)

# Authorize the client
client = gspread.authorize(creds)

# Access the sheet
sheet = client.open("판매대장").sheet1

# Read data into pandas dataframe
data = sheet.get_all_records()
df = pd.DataFrame(data)