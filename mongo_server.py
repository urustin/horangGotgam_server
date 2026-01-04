import pymongo
import sys
import certifi
from pymongo import MongoClient
import ssl
import os
from dotenv import load_dotenv


#.env
load_dotenv()

#load variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PWD= os.getenv("MONGO_PWD")
MONGO_CLUSTER= os.getenv("MONGO_CLUSTER")
MONGO_DB= os.getenv("MONGO_DB")




def get_client(host, username, password, db):
    # Note: Removed 'port' parameter because the 'mongodb+srv://' URI format used with Atlas does not require a port.
    # Adjust the connection string as needed for your specific MongoDB setup.
    connection_string = f'mongodb+srv://{username}:{password}@{host}/{db}?retryWrites=true&w=majority'
    return MongoClient(connection_string, tlsCAFile=certifi.where())

# # client = get_client("host-ip","port","username","password","db-name")
# 접속 정보를 매번 입력하지 않도록 헬퍼 함수를 만들면 편합니다.
def get_db_connection():
    client = get_client(MONGO_CLUSTER, MONGO_USER, MONGO_PWD, MONGO_DB)
    return client[MONGO_DB]


def load_order():
    # client = get_client("host", "id", "pwd", "horanggotgam")
    # db = client.horanggotgam
    db = get_db_connection()
    collection = db["orderList_options"] 
    cursor = collection.find()
    # print(cursor)
    # Loop through the cursor to print each document
    documents ={
        "currentYear" : cursor[0]['currentYear'],
        "availableDate" : cursor[0]['availableDate'],
        "orderAvailable" : cursor[0]['orderAvailable'],
        "product1" : cursor[0]['product1'],
        "product2" : cursor[0]['product2'],
        "product3" : cursor[0]['product3'],
        "product4" : cursor[0]['product4'],
        "product5" : cursor[0]['product5'],
    }
    # print(documents)
    # docu
    # for document in cursor:
        # print(document)
    return documents
# test
load_order()

def update_order(newValue):
    db = get_db_connection()
    collection = db["orderList_options"] 

    filter = {}
    # Values to be updated.
    newvalues = {
        "$set": newValue
    }
    # Using update_one() method for single 
    # updation.
    collection.update_one(filter, newvalues)
    return 0

 
def update_date(newValue):
    db = get_db_connection()
    collection = db["orderList_options"] 

    filter = {}
    # Values to be updated.
    newvalues = {
        "$set": {'availableDate': newValue.get('availableDate')}
    }
    # Using update_one() method for single 
    # updation.
    collection.update_one(filter, newvalues)
    return 0

def delete_date(newValue):
    db = get_db_connection()
    collection = db["orderList_options"] 

    filter = {}
    # Values to be updated.
    newvalues = {
        "$pull": {"availableDate":newValue.get('availableDate')}
    }
    result = collection.update_one(filter, newvalues)
    return result.modified_count > 0

 





