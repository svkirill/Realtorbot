import os
import json

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    @staticmethod
    def Deserialize(data: dict):
        user = User(data.get("chat_id"))
        return user
class UserService:
    users = []
    storagePath = "Storage/users.json"

    @staticmethod
    def FindUser(chat_id):
        for user in UserService.users:
            if user.chat_id == chat_id:
                return chat_id
        return None

    @staticmethod
    def GetUser(chat_id):
        user = UserService.FindUser(chat_id)

        if user == None:
            user = User(chat_id)
            UserService.users.append(user)

            UserService.SaveUsersToJson()

        return user



    @staticmethod  # TODO - бд
    def SaveUsersToJson():
        realtors = []
        saveRealtors = {"objects": realtors}

        for realtor in UserService.users:
            realtors.append(realtor.__dict__)

        print(saveRealtors)
        with open(UserService.storagePath, 'w') as file:
            json.dump(saveRealtors, file)

    @staticmethod  # TODO - бд
    def LoadDataFromJson():
        if os.path.exists(UserService.storagePath):
            with open(UserService.storagePath, 'r') as file:
                data = json.load(file)

                realtors = data.get("objects", [])  # [] - default value
                result = []

                for realtorDict in realtors:
                    result.append(User.Deserialize(realtorDict))

                return result
        return []

    @staticmethod
    def InitData():
        UserService.users = UserService.LoadDataFromJson()