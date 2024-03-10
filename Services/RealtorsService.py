from Services.UserInputService import UserInputService
from Models.Realtor import Realtor
import json
import os.path
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton

class RealtorsService:
    # key: chat_id, value : (key: data_name, value: data)
    realtors = []  # TODO - вынесение
    storagePath = "Storage/realtors.json"

    @staticmethod
    def process_realtor_data(chatid):  # TODO - вынесение в класс пользовательского ввода
        context: dict = UserInputService.get_user_input(chatid)

        if context is not None:
            realtor = Realtor(context.get('name'), context.get('phonenumber'))
            RealtorsService.realtors.append(realtor)
            RealtorsService.SaveRealtorToJson()

    @staticmethod
    def get_realtors_menu(startIndex, endIndex, pageNumer, pageSize=5):
        keyboard = ReplyKeyboardMarkup()

        for realtor in RealtorsService.realtors:
            text = f"{realtor.name} {realtor.surname}"
            button = KeyboardButton(text=text)
            keyboard.add(button)

        return keyboard

    @staticmethod   # TODO - бд
    def SaveRealtorToJson():
        realtors = []
        saveRealtors = {"objects": realtors}

        for realtor in RealtorsService.realtors:
            realtors.append(realtor.__dict__)

        print(saveRealtors)
        with open(RealtorsService.storagePath, 'w') as file:
            json.dump(saveRealtors, file)

    @staticmethod   # TODO - бд
    def LoadDataFromJson():
        if os.path.exists(RealtorsService.storagePath):
            with open(RealtorsService.storagePath, 'r') as file:
                data = json.load(file)

                realtors = data.get("objects", [])  # [] - default value
                result = []

                for realtorDict in realtors:
                    result.append(Realtor.Deserialize(realtorDict))

                return result
        return []

    @staticmethod
    def InitData():
        RealtorsService.realtors = RealtorsService.LoadDataFromJson()


if __name__ == "__main__":
    UserInputService.user_input["123"] = {"name": "Ivan", "phonenumber": 78127283213}
    RealtorsService.storagePath = "../Storage/realtors_test.json"
    RealtorsService.process_realtor_data("123")