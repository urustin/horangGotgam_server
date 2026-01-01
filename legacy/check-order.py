# app.py

from flask import Flask, request, render_template_string
from flask_cors import CORS  # Import CORS
from flask import jsonify
import google_sheets


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/submit', methods=['POST'])
def submit():
    # load horang gotgam doc
    sheet_id ="1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8" #2024
    # sheet_id ="1l9L622elcowuHiM1gyOrtVaZZX-tWmhIUibx4rEHdww" #2023

    # get the name and number from web
    name = request.form['name']
    phoneNumber = request.form['phoneNumber']
    

    # Use the Google Sheets module to append data
    
    # google_sheets.test_print()

    # print(google_sheets.get_data(sheet_id,'A1:H10'))

    # google_sheets.append_data(sheet_id, [name, phoneNumber])

    row_number, row_data = google_sheets.find_row_by_phone_and_name(sheet_id, phoneNumber, name)
    print(row_data)
    # if row_number:
    #     return f"Match found at row {row_number}: {row_data}"
    # else:
    #     return "No match found"

    if row_number:
        formatted_data = ', '.join(row_data)
        return formatted_data
    else:
        return "No match found"



@app.route('/check-order')
def check_order():
    # Fetch data pick year
    # sheet_id ="1l9L622elcowuHiM1gyOrtVaZZX-tWmhIUibx4rEHdww" #2023
    sheet_id ="1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8" #2024


    name = request.args.get('name')
    phoneNumber = request.args.get('phoneNumber')

    matches = google_sheets.find_rows_by_phone_and_name(sheet_id, phoneNumber, name)

    if matches:
        orders = []
        for match in matches:
            order = {
                "expected_date": match[1],
                "send_name": match[6],
                "send_contact": match[7],
                "rcv_name": match[8],
                "rcv_contact": match[9],
                "rcv_address": match[10],
                "orderList": match[14:19],  # Adjust indices as needed
                "totalFee": match[22]
            }
            orders.append(order)
        return jsonify(orders)
    else:
        return jsonify({"error": "오류가 발생하였습니다! 번호를 다시한번 확인해주세요!"})
    

if __name__ == '__main__':
    app.run(debug=True, port=5007)


