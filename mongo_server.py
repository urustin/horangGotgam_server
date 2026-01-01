import pymongo
import sys
import certifi
from pymongo import MongoClient
import ssl



# client = pymongo.MongoClient("mongodb+srv://urustin:asdf1234@cluster0.eonroyn.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())


def get_client(host, username, password, db):
    # Note: Removed 'port' parameter because the 'mongodb+srv://' URI format used with Atlas does not require a port.
    # Adjust the connection string as needed for your specific MongoDB setup.
    connection_string = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
        username, password, host, db
    )
    return MongoClient(connection_string, tlsCAFile=certifi.where())

# # client = get_client("host-ip","port","username","password","db-name")


def load_order():
    client = get_client("cluster0.eonroyn.mongodb.net", "urustin", "asdf1234", "horanggotgam")
    db = client.horanggotgam
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
    client = get_client("cluster0.eonroyn.mongodb.net", "urustin", "asdf1234", "horanggotgam")
    db = client.horanggotgam
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
    client = get_client("cluster0.eonroyn.mongodb.net", "urustin", "asdf1234", "horanggotgam")
    db = client.horanggotgam
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
    client = get_client("cluster0.eonroyn.mongodb.net", "urustin", "asdf1234", "horanggotgam")
    db = client.horanggotgam
    collection = db["orderList_options"] 

    filter = {}
    # Values to be updated.
    newvalues = {
        "$pull": {"availableDate":newValue.get('availableDate')}
    }
    result = collection.update_one(filter, newvalues)
    return result.modified_count > 0

 





