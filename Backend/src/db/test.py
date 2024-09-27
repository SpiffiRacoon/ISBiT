import pymongo


# client = pymongo.MongoClient(
#     '192.168.68.100',
#     # 'mongodb://localhost',
#     username='',
#     password='',
#     port=27017,
#     authSource="admin",
# )

client = pymongo.MongoClient("localhost", port=27017)
db = client.isbit

test = db["test"]

# test.insert_one({"test": "first"})
for obj in test.find():
    print(obj)

# print("Here ok")
# mydb = client["isbit"]

# mycol = mydb["test"]

# mydict = { "name": "John", "address": "Highway 37" }

# print("Still ok")
# x = mycol.insert_one(mydict)

# client.close()
