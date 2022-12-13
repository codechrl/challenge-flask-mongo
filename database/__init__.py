from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

try:
    conn = MongoClient("mongodb+srv://mongo:hehe@cluster0.2rd5qqp.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    print("INFO\tDatabase Connected successfully!!!")
except Exception as e:  
    print("INFO\tCould not connect to MongoDB")
    print("ERROR\t",e)

db = conn['inagri_test']