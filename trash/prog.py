# from dataFile import programming


# print([x[::-1] for x in programming.keys()])
import pymongo
from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('zen')
password = urllib.parse.quote_plus("shared123")

url = "mongodb+srv://{}:{}@cluster0-0000.mongodb.net/<dbname>?retryWrites=true&w=majority".format(username, password)
# url is just an example (your url will be different)

print(url)

# cluster = MongoClient(url)
# db = cluster['Sample']
# collection = db['temporary']