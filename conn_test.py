import pymongo
import datetime
import bcrypt

from pymongo import MongoClient

#MongoDB connection using cluster's connection string
client = pymongo.MongoClient("mongodb+srv://radhika:Radhika1997@simplii.tvhh1.mongodb.net/simplii?retryWrites=true&w=majority")

#database to which connections are to be made, here the name of our database is "simplii"
db = client.simplii

#testing of password hashing for security purposes
password = "abcd1234"
hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashAndSalt)
# save "hashAndSalt" in database

# To check:
# password = userInput
valid = bcrypt.checkpw(password.encode(), hashAndSalt)
print(valid)

#testing of sample/dummy data insertion
#input to be taken from login/sign up form once created
'''
user1 = {
    "user_id": "Radhika20",
    "first_name":"Radhika",
    "last_name":"Raman",
    "email_id":"rbraman@ncsu.edu",
    "password":"sdfsdf"
}


testUserInfo = db.testUserInfo
result = testUserInfo.insert_one(user1)
print(f"User 1: {result.inserted_id}")

'''

