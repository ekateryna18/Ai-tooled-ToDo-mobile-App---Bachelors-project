import bcrypt
from bson import ObjectId

class UserRepository:
    def __init__(self, database, salt):
        self.__database__ = database
        self.__users__ = self.__database__.users
        self.__salt__ = salt

    def add(self,user):
        bytes_pw = user.password.encode('utf-8')
        password = bcrypt.hashpw(bytes_pw, bytes(self.__salt__, encoding='utf8')).decode('utf-8')
        self.__users__.insert_one({
            "username": user.username,
            #"password": user.password
            "password": password
        })

    def find_one_by_username(self,username):
        cursor = list(self.__users__.find({'username': username}))
        if len(cursor) == 0:
            return None
        user = cursor[0]
        return user