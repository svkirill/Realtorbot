import os
import json
from Models.User import User
from telebot.types import Message

class UserService:
    users = []
    storagePath = "Storage/users.json"

    @staticmethod
    def FindUser(chat_id):
        for user in UserService.users:
            if user.chat_id == chat_id:
                return user
        return None

    @staticmethod
    def GetUserByContext(message : Message):
        user = UserService.FindUser(message.chat.id)

        if user == None:
            user = User(message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.language_code)
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