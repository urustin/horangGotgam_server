# horang-app.py

import os
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS  # Import CORS
import google_sheets
import google_ocr
import mongo_server
# log
# import logging

#sheet id
# SHEET_ID = "1TgP00ffU5Mx79chhjPLUTU1s00jIIT65fRUj7Ju6Q4A" #2025
SHEET_ID = "1iE7yyfargHRgU9IAaM_qCoaKM5BnDn-DnUwvmUmtOSg" #2026
SHEET_ID_DURUP = "1ZED9Jng66YtovQmNaf5k0EJ0qIkkQfoW19T4edAyl3g" #2025_durup    

# logging.basicConfig(filename='/home/ubuntu/.pm2/logs/horang-checkOrder.log', level=logging.INFO)
# logging.basicConfig(filename='./test.log', levela=logging.INFO)
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/check-order')
def check_order():
    # Fetch data pick year
    sheet_id = SHEET_ID

    
    name = request.args.get('name')
    phoneNumber = request.args.get('phoneNumber')
    
    # Log every request
    # logging.info(f"Received request for /check-order with name: {name} and phoneNumber: {phoneNumber}")

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
                "orderList": match[14:19],
                # "totalFee": match[22]
            }
            orders.append(order)
        return jsonify(orders)
    else:
        return jsonify({"error": "오류가 발생하였습니다! 번호를 다시한번 확인해주세요!"})
    


# index2

@app.route('/count-box')
def count_box():

    
    formattedDate = request.args.get('formattedDate')
    print("formatDate==",formattedDate)
    
    # finding thing
    # sheet_id ="1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8" #2024
    # print(google_sheets.convert_date_to_korean_weekday("1/4"))
    # keyword = google_sheets.convert_date_to_korean_weekday("1/10")
    # position = google_sheets.check_position(sheet_id, keyword)
    # if position:
    #     print(f"Keyword '{keyword}' found at position: {position}")
    # else:
    #     print(f"Keyword '{keyword}' not found in the sheet.")
    
    # main reload
    # sheet_id ="1Z8gLLzjTR13rxNvkou0WWvbqVHZQFfFr3gOWJHVfae8" #2024
    sheet_id = SHEET_ID
    searchDate = google_sheets.convert_date_to_korean_weekday(formattedDate)
    data = google_sheets.get_filtered_data_by_date(sheet_id, searchDate)
    # print(data)
    # data = google_sheets.get_filtered_data(sheet_id, start_text, end_text, column)
    result = google_sheets.aggregate_box_data(data)
    # print("final======",result)
    return jsonify(result)



@app.route('/get-all-data')
def get_all_data_route():

    formattedDate = request.args.get('formattedDate')
    print("formatDate==",formattedDate)
    
    sheet_id = SHEET_ID
    # all_data = google_sheets.get_all_data(sheet_id)

    searchDate = google_sheets.convert_date_to_korean_weekday(formattedDate)
    # data = google_sheets.get_filtered_data_ascending(sheet_id, searchDate)
    data = google_sheets.get_filtered_data_by_date(sheet_id, searchDate)

    return jsonify(data) 



# index5
@app.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.json
    print(data)

    sheet_id =SHEET_ID
    
    # name = request.args.get('name')
    google_sheets.append_data(sheet_id, data["sheetName"], data)
    # print(google_sheets.get_data(sheet_id,"A1:B10"))
    
    return jsonify(data)

# durup


@app.route('/submit-order-durup', methods=['POST'])
def submit_order_durup():
    data = request.json
    print(data)

    # sheet_id ="1l9L622elcowuHiM1gyOrtVaZZX-tWmhIUibx4rEHdww" #2023
    # sheet_id = "1FA_93rAknkh_Q4W1SHGOhiRL3oE9-u-6ACYAnSbtmBM" #test
    # sheet_id ="1uVpFnvJ3zuW48AjA_rgf2epE_FQUKVg9yAIU4JGGLSY" #2024_durup
    sheet_id =SHEET_ID_DURUP

    # name = request.args.get('name')
    google_sheets.append_data(sheet_id, data["sheetName"], data)
    # print(google_sheets.get_data(sheet_id,"A1:B10"))
    
    return jsonify(data)

# typeOrder
@app.route('/image-text', methods=['POST'])
def image_text():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Temporary save or direct read
        # To directly read the file content without saving, use:
        # file_content = file.read()
        # data = google_ocr.detect_text_content(file_content)
        
        # To save temporarily and then process, use:
        temp_path = os.path.join('/tmp', file.filename)
        file.save(temp_path)
        data = google_ocr.detect_text(temp_path)
        
        # Optionally, remove the file if you saved it temporarily
        os.remove(temp_path)

        return jsonify(data)


# controlMenu
@app.route('/load-order')
def load_order():
    data = mongo_server.load_order()
    return jsonify(data)
    # return data

@app.route('/update-order', methods=['POST'])
def update_order():
    data = request.json
    # print(data["currentYear"])
    mongo_server.update_order(data)


    return data


@app.route('/add-date', methods=['POST'])
def add_date():
    data = request.json
    # print(data["currentYear"])
    mongo_server.update_date(data)
    # print(data)
    return data


@app.route('/delete-date', methods=['POST'])
def delete_date():
    data = request.json

    result = mongo_server.delete_date(data)

    if result:
        return jsonify({"success": True, "message": "Date removed successfully"}), 200
    else:
        return jsonify({"success": False, "message": "Error removing date"}), 500
    return 0


@app.route('/test', methods=['GET'])
def test():
    print("test")
    sheet_id =SHEET_ID 
    # 모든 데이터를 불러옵니다.
    all_data = google_sheets.get_all_data(sheet_id)

    # 결과 출력
    if all_data:
        for row in all_data[0:10]:
            print(row)
    else:
        print("데이터를 불러오는 데 실패했습니다.")
    
    return all_data[0:10]

# test()

# port 5008


if __name__ == '__main__':
    app.run(debug=False, port=5008)


#open to 0.0.0.0
# if __name__ == '__main__':
#     # host='0.0.0.0'을 추가해야 외부(공유기, 다른 PC)에서 접속 가능합니다.
#     app.run(host='0.0.0.0', debug=True, port=5008)

