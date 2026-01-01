# google_sheets.py

import gspread
from google.oauth2.service_account import Credentials

def init_client():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file('./haranggotgam-22ece62e15d4.json', scopes=scope)
    return gspread.authorize(creds)

def get_data(sheet_id, range):
    client = init_client()
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet.get(range)

def append_data(sheet_id, data):
    client = init_client()
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.append_row(data)

def test_print():
    print("testWork")

# single
# def find_row_by_phone_and_name(sheet_id, phone_number, name):
#     client = init_client()
#     sheet = client.open_by_key(sheet_id).sheet1

#     # Column G for names (7th column) and Column H for phone numbers (8th column)
#     phone_col = sheet.col_values(8)  # 8th column for phone numbers
#     for i, phone in enumerate(phone_col, start=1):  # start=1 for 1-indexed row numbers
#         if phone == phone_number:
#             row = sheet.row_values(i)
#             if row[6] == name:  # 6th index for names in the row list
#                 return i, row  # Return row number and data
#     return None, None  # Return None if no match is found


# find multi item

def find_rows_by_phone_and_name(sheet_id, phone_number, name):
    client = init_client()
    spreadsheet = client.open_by_key(sheet_id)

    # tab1
    sheet = client.open_by_key(sheet_id).sheet1

    # tab2
    # sheet = spreadsheet.worksheet('Sheet2')

    # Column G for names (7th column) and Column H for phone numbers (8th column)
    phone_col = sheet.col_values(8)
    name_col = sheet.col_values(7)
    
    matches = []

    for i, phone in enumerate(phone_col):
        # Extract last 4 digits of the phone number
        phone_last4 = phone[-4:] if len(phone) >= 4 else ""
        
        if phone_last4 == phone_number and name_col[i] == name:
            row = sheet.row_values(i + 1)  # +1 because sheet rows are 1-indexed
            matches.append(row)

    return matches
