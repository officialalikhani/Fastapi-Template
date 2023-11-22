import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


class MongoDb:
    def __init__(self):
        self.myclient = pymongo.MongoClient(
            os.getenv("MONGO_ADDR"),
            username=os.getenv("MONGO_USER"),
            password=os.getenv("MONGO_PASSWD"),
        )
        self.mydb = self.myclient["MyDB"]
        self.MyCollection = self.mydb["MyCollection"]

    def select_user_by(self, username):
        user = self.MyCollection.find_one({f"{username}.username": f"{username}"})
        return user

    def user_mongo(self, user, userhash, role):
        general = {
            user: {
                "username": user,
                "full_name": user,
                "hashed_password": userhash,
                "role": role,
            }
        }
        self.MyCollection.insert_one(general)
