from pymongo import MongoClient


def getCollection():
    client = MongoClient("localhost", 27017)
    db = client.publixdb
    bogo = db.bogo

    return bogo

def deleteItems():
    bogo = getCollection()
    bogo.delete_many({})

def printItems():
    bogo = getCollection()

    print(f"Number of BOGO items: {bogo.count_documents({})}\n")

    for item in bogo.find():
        print(item["item_name"])