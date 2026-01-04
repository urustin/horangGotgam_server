# google_sheets.py
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz



# check-order start
def init_client():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file('./auth/horang-gotgam-df58ef690daa.json', scopes=scope)
    return gspread.authorize(creds)

def get_data(sheet_id, range):
    print("get_data")
    client = init_client()
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet.get(range)

def append_data(sheet_id, sheetName, data):
    # print("append_data")
    client = init_client()
    sheet = client.open_by_key(sheet_id).worksheet(sheetName)

    # data preprocess
    data['send_contact'] = str(data['send_contact'])
    data['rcv_contact'] = str(data['rcv_contact'])
    
    kst = pytz.timezone('Asia/Seoul')
    current_time_kst = datetime.now(kst)
    formatted_time_kst = current_time_kst.strftime("%Y. %m. %d %p %I:%M:%S")


    # Handle product quantities based on product type
    if data['productType'] == 'gotgam':
        product1 = int(data['product1']) if data['product1'] != '' else ""
        product2 = int(data['product2']) if data['product2'] != '' else ""
        product3 = int(data['product3']) if data['product3'] != '' else ""
        product4 = int(data['product4']) if data['product4'] != '' else ""
        product5 = int(data['product5']) if data['product5'] != '' else ""
        row_data = [
            #0 =타임스탬프
            formatted_time_kst,
            #1배송예약날짜
            data['reserveDate'],
            #234, 배송입금확인
            "","","",
            #5 경로
            "",
            #6 주문자 성함
            data['send_name'],
            #7 주문자 연락처
            int(data['send_contact']),
            #8 받는분 성함
            data['rcv_name'],
            #9 받는분 연락처
            int(data['rcv_contact']),
            #10 받는분 주소
            data['rcv_address'],
            #11 배송요청사항
            data['request_delivery'],
            #12 
            "",
            #13 기타 요청사항
            data['request_etc'],
            #14 1호
            product1,
            #15 2호
            product2,
            #16 3호
            product3,
            #17 4호
            product4,
            #18 5호
            product5,
            #19 기타
            "",
            data['totalAmount']
        ]
        
    else:  # durup
        product1 = int(data['durup1']) if data['durup1'] != '' else ""
        product2 = int(data['durup2']) if data['durup2'] != '' else ""
        product3 = ""
        product4 = ""
        product5 = ""
        row_data = [
            #1 =타임스탬프
            formatted_time_kst,
            #2배송예약날짜
            data['reserveDate'],
            #345, 배송입금확인
            "","","",
            #6 경로
            "",
            #7 주문자 성함
            data['send_name'],
            #8 주문자 연락처
            int(data['send_contact']),
            #9 받는분 성함
            data['rcv_name'],
            #10 받는분 연락처
            int(data['rcv_contact']),
            #11 받는분 주소
            data['rcv_address'],
            
            #공백 필요
            "",
            "",
            #12 배송요청사항
            data['request_delivery'],
            #13 기타요청 (두릅)
            data['request_etc'],
            #14 1호
            product1,
            #15 2호
            product2,
            #16 3호
            product3,
            #17 4호
            product4,
            #18 총액
            data['totalAmount'],

        ]

    
    

    try:
        sheet.append_row(row_data, table_range="A4")
    except Exception as e:
        print("Error appending data:", e)
        raise

# find multi item

def find_rows_by_phone_and_name(sheet_id, phone_number, name):
    client = init_client()
    # spreadsheet = client.open_by_key(sheet_id)

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


#check-order end



#count-box start
def column_to_index(column_letter):
    print("column_to_index")
    # Convert a spreadsheet column letter to an integer index (0-based)
    print("column_to_index",ord(column_letter.upper()) - ord('A'))
    return ord(column_letter.upper()) - ord('A')

def get_filtered_data_by_date(sheet_id, date_string):
    print("get_filtered_data_by_date")
    client = init_client()
    sheet = client.open_by_key(sheet_id).sheet1
    print(date_string)
    # date_string = convert_date(date_string)
    # print(date_string)
    # Get all values (returns data as a list of lists)
    all_values = sheet.get_all_values()

    # The date column is fixed to the second column (column B)
    date_column_index = 1  # Column index for 'B' (0-based indexing)

    # The first row is assumed to be the header
    data = all_values[1:]

    # List to store rows that match the date
    matching_rows = []

    # Search for rows that match the given date string
    print("AA")
    # print(data[0:5])
    print("bb")
    for row in data:
        # print(row[date_column_index])
        if row[date_column_index] == date_string:
            
            matching_rows.append(row)

    # Return the list of matching rows
    return matching_rows

    

def aggregate_box_data(data):
    box_count = {}

    # Columns for box types quantities (O, P, Q, R, S)
    box_type_columns = {
        '1': 14,  # Column O
        '2': 15,  # Column P
        '3': 16,  # Column Q
        '4': 17,  # Column R
        '5': 18,  # Column S
    }

    for row in data:
        # print("row=",row)
        if not any(row):
            continue

        for box_type, col_index in box_type_columns.items():
            # print("box_type=",box_type)
            # print("col_index=",col_index)
            # print("box_type_columns=",box_type_columns)
            # print("row[col_index]=",row[col_index])
            # strip = remove whitespace
            quantity_str = row[col_index].strip()

            if quantity_str.isdigit():
                quantity = int(quantity_str)
                key = f"{box_type}_{quantity}"
                box_count[key] = box_count.get(key, 0) + 1
                # print("!!box_count=",box_count)
            # else:
                # print(f"Non-numeric or empty quantity '{quantity_str}' in row: {row}")

    return box_count



# for check /debug

def check_position(sheet_id, keyword):
    client = init_client()
    sheet = client.open_by_key(sheet_id).sheet1
    all_values = sheet.get_all_values()
    
    for row_idx, row in enumerate(all_values):
        for col_idx, cell in enumerate(row):
            if cell == keyword:
                # Convert column index to letter (1-indexed to match spreadsheet convention)
                col_letter = chr(col_idx + ord('A'))
                return f"{col_letter}{row_idx + 1}"
    return None



# date to string( 1/9 화)



def convert_date_to_korean_weekday(date_str):
    # Use the current year
    year = datetime.now().year
    
    # Split the input date string to get the month and day
    month, day = date_str.split('/')

    # Create a date string with the current year and the provided month and day
    formatted_date_str = f"{year}-{month}-{day}"

    # Convert the string to a datetime object
    date_obj = datetime.strptime(formatted_date_str, '%Y-%m-%d')

    # Get the weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)
    weekday = date_obj.weekday()

    # Mapping of weekdays from number to Korean abbreviation
    korean_weekdays = ["월", "화", "수", "목", "금", "토", "일"]

    # Return the date in the desired format
    return f"{month}월 {day}일({korean_weekdays[weekday]})"




# index3.html

def get_all_data(sheet_id):
    client = init_client()
    sheet = client.open_by_key(sheet_id).sheet1
    all_rows = sheet.get_all_values()
    # print("all_rows= ", all_rows)
    return all_rows


# get filter to ascending

def get_filtered_data_ascending(sheet_id, date_string):
    print("ascending")
    client = init_client()
    sheet = client.open_by_key(sheet_id).sheet1

    # Get all values (returns data as a list of lists)
    all_values = sheet.get_all_values()

    # The date column is fixed to the second column (column B)
    date_column_index = 1  # Column index for 'B' (0-based indexing)

    # The first row is assumed to be the header
    data = all_values[1:]

    # List to store rows that match the date
    matching_rows = []

    # Search for rows that match the given date string
    for row in data:
        if row[date_column_index] == date_string:
            matching_rows.append(row)

    filter1_rows = []
    filter2_rows = []
    for row in matching_rows:
        count = 0
        
        for i in range(14,20):
            if row[i] != "":
                count=count+1


        if(count==1):
            filter1_rows.append(row)
        else:
            filter2_rows.append(row)
    
    print("filter1= ",filter1_rows)
    print("filter2= ",filter2_rows)

    total_rows = []
    total_rows.append(filter1_rows)
    # total_rows.append(filter2_rows)


    # Return the list of matching rows
    return total_rows



# 날짜 변환 함수 정의
def convert_date(date_str):
    year = 2025
    # 문자열을 "월/일"로 파싱하여 datetime 객체 생성
    parsed_date = datetime.strptime(date_str, "%m/%d")
    # 2025년을 추가하여 새로운 날짜 생성
    return f"{year}-{parsed_date.month}-{parsed_date.day}"

#test
# def get_all_data(sheet_id):
#     try:
#         client = init_client()
#         spreadsheet = client.open_by_key(sheet_id)
#         sheet = spreadsheet.worksheet("응답")
#         all_data = sheet.get_all_values()  # 시트의 모든 데이터를 불러옵니다.
#         return all_data
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return None