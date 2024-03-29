from Services.UserInputService import UserInputService
from Models.Realtor import Realtor
import json
import os.path
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton

class RealtorsService:
    # key: chat_id, value : (key: data_name, value: data)
    realtors = []  # TODO - вынесение
    storagePath = "Storage/realtors.json"
    NOT_VISIBLE_SYMBOL = "ㅤ"
    NEXT_TEXT = "Далее"
    BACK_TEXT = "Назад"

    @staticmethod
    def process_realtor_data(chatid):  # TODO - вынесение в класс пользовательского ввода
        context: dict = UserInputService.get_user_input(chatid)

        if context is not None:
            realtor = Realtor(context.get('name'), context.get('phonenumber'))
            RealtorsService.realtors.append(realtor)
            RealtorsService.SaveRealtorToJson()

    @staticmethod
    def get_realtors_menu(pageNumber, pageSize=5):
        keyboard = ReplyKeyboardMarkup()
        endIndex = pageNumber * pageSize - 1
        startIndex = endIndex - (pageSize - 1)
        for realtor in RealtorsService.realtors[startIndex:endIndex+1]:
            text = f"{realtor.name} {realtor.surname}"
            button = KeyboardButton(text=text)
            keyboard.add(button)

        # Добавляем кнопку далее, если это необходимо
        nextText = RealtorsService.NEXT_TEXT
        if endIndex >= len(RealtorsService.realtors) - 1:
            nextText = RealtorsService.NOT_VISIBLE_SYMBOL

        btn_next = KeyboardButton(text=nextText)

        # Добавляем кнопку назад, если это необходимо
        backText = RealtorsService.BACK_TEXT
        if pageNumber <= 1:
            backText = RealtorsService.NOT_VISIBLE_SYMBOL

        btn_back = KeyboardButton(text=backText)

        keyboard.add(btn_back,btn_next)

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