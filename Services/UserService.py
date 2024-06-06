import os
import json
from Sqlite.realtorss import User
from telebot.types import Message

class UserService:
    #users = []
    #storagePath = "Storage/users.json"

    @staticmethod
    def GetUsers():
        return User.select()

    @staticmethod
    def FindUser(chat_id):
        for user in User.select():
            if user.chat_id == chat_id:
                return user
        return None

    @staticmethod
    def GetUserByContext(message : Message):
        user = UserService.FindUser(message.chat.id)

        if user == None:
            print(f"User will be created")
            user = User.create(chat_id = message.chat.id, username = message.from_user.username, first_name = message.from_user.first_name,last_name = message.from_user.last_name,language_code = message.from_user.language_code)
            #UserService.users.append(user)

            print(f"User created {user.role.name} {user.chat_id}")

            #UserService.SaveUsersToJson()

        return user

    '''@staticmethod  # TODO - бд
    def SaveUsersToJson():
        realtors = []
        saveRealtors = {"objects": realtors}

        for realtor in UserService.users:
            realtors.append(realtor.__dict__)

        print(saveRealtors)
        with open(UserService.storagePath, 'w') as file:
            json.dump(saveRealtors, file)'''

    '''@staticmethod  # TODO - бд
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
        UserService.users = UserService.LoadDataFromJson()'''