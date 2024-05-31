from Services.UserInputService import UserInputService
from Models.Realtor import Realtor, RealtorHelper
import json
import os.path
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from Services.CompanyService import CompanyService

class RealtorsService:
    # key: chat_id, value : (key: data_name, value: data)
    realtors = []  # TODO - вынесение
    storagePath = "Storage/realtors.json"
    NOT_VISIBLE_SYMBOL = "ㅤ"
    NEXT_TEXT = "Далее👉"
    BACK_TEXT = "👈Назад"
    backmenuu = 'Вернуться в главное меню'

    DEFAULT_PAGE_SIZE = 5
    CHANGE_NAME_PARAM = "ChangeName"
    CHANGE_SURNAME_PARAM = 'ChangeSurname'
    CHANGE_PHONENUMBER_PARAM = 'ChangePhoneNumber'
    CHANGE_SELFEMPLOYED_PARAM = 'ChangeSelfEmployed'
    CHANGE_COMPANY_PARAM = "ChangeCompany"

    @staticmethod
    def process_realtor_data(chatid):  # TODO - вынесение в класс пользовательского ввода
        context: dict = UserInputService.get_user_input(chatid)

        if context is not None:
            realtor = Realtor(context.get('name'), context.get('phonenumber'))
            RealtorsService.realtors.append(realtor)
            RealtorsService.SaveRealtorToJson()

    @staticmethod
    def GetRealtorInfo(btn_text):
        textForUser = None

        uniqueCode = RealtorHelper.GetUniqueCode(btn_text)
        realtor: Realtor = RealtorsService.FindbyCode(uniqueCode)
        company = CompanyService.FindCompanyById(realtor.companyId)

        if realtor != None:
            textForUser = f"{realtor.name}\n{len(realtor.name)*'-'}\n"
            textForUser += f"Phone number: {realtor.phoneNumber}\n"

            if company is not None:
                textForUser += f"Company: {company.name} ({company.phonenumber})\n"

            if realtor.selfemployed:
                textForUser += f"Is self employed.\n"

        return textForUser

    @staticmethod
    def FindbyCode(code):
        for realtor in RealtorsService.realtors:
            if realtor.GetUniqueCode() == code:
                return realtor
        return None

    @staticmethod
    def AddReviewToRealtor(review, code):
        if review != None and review != "" and code != None and code != "":
            realtor : Realtor = RealtorsService.FindbyCode(code)

            if realtor != None:
                realtor.reviews.append(review)
                RealtorsService.SaveRealtorToJson()

                return True

        return False

    @staticmethod
    def ChangeRaltorParam(uniqueCode, paramName, newValue):
        # вытасикваешь риэлтора по уникальному коду
        realtor : Realtor = RealtorsService.FindbyCode(uniqueCode)

        if realtor is not None:
            # меняешь в зависимости от paramName нужный параметр
            if paramName == RealtorsService.CHANGE_NAME_PARAM:
                realtor.name = newValue

            elif paramName == RealtorsService.CHANGE_SURNAME_PARAM:
                realtor.surname = newValue

            elif paramName == RealtorsService.CHANGE_PHONENUMBER_PARAM:
                realtor.phoneNumber = newValue

            # Сохраняешь всех риэлторов
            RealtorsService.SaveRealtorToJson()

            return realtor.GetUniqueCode()

        return None

    @staticmethod
    def CheckRealtorInPage(uniqueCode, pageNumber):
        pageSize = RealtorsService.DEFAULT_PAGE_SIZE
        endIndex = pageNumber * pageSize - 1
        startIndex = endIndex - (pageSize - 1)

        for foundrealtor in RealtorsService.realtors[startIndex:endIndex + 1]:
            if uniqueCode == foundrealtor.GetUniqueCode():
                return (pageNumber, True)

        return (pageNumber, False)

    @staticmethod
    def get_realtors_menu(pageNumber, pageSize=None):
        if pageSize is None:
            pageSize = RealtorsService.DEFAULT_PAGE_SIZE

        keyboard = ReplyKeyboardMarkup()
        endIndex = pageNumber * pageSize - 1
        startIndex = endIndex - (pageSize - 1)
        for realtor in RealtorsService.realtors[startIndex:endIndex+1]:
            text = realtor.GetUniqueDescription()
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

        btn_menu = RealtorsService.backmenuu

        button_backmenu = KeyboardButton(text=btn_menu)
        keyboard.add(button_backmenu)

        return keyboard

    @staticmethod   # TODO - бд
    def SaveRealtorToJson():
        realtors = []
        saveRealtors = {"objects": realtors}

        for realtor in RealtorsService.realtors:
            realtors.append(realtor.__dict__)


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
    def check_new_info_realtor():
        pass


    @staticmethod
    def InitData():
        RealtorsService.realtors = RealtorsService.LoadDataFromJson()


if __name__ == "__main__":
    UserInputService.user_input["123"] = {"name": "Ivan", "phonenumber": 78127283213}
    RealtorsService.storagePath = "../Storage/realtors_test.json"
    RealtorsService.process_realtor_data("123")