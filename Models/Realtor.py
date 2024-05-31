import base64
import telebot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
class RealtorHelper:
    @staticmethod
    def GetUniqueCode(data):
        dataBytes = data.encode('utf-8')  # bytes
        base64_bytes = base64.b64encode(dataBytes)
        base64_text = base64_bytes.decode('utf-8')
        return base64_text

class Realtor:
    def __init__(self,name, phoneNumber, surname=""):
        self.name = name
        self.phoneNumber = phoneNumber
        self.surname = surname
        self.reviews = []   # TODO - возможно нужно завести класс
        self.companyId = 0
        self.selfemployed = True

    def GetUniqueCode(self):
        data = self.GetUniqueDescription()
        code = RealtorHelper.GetUniqueCode(data)
        return code

    def GetUniqueDescription(self):
        keyboard = InlineKeyboardButton
        return f"{self.name} - {self.surname} - {self.phoneNumber}"



    @staticmethod
    def Deserialize(data : dict):
        realtor = Realtor(data.get("name"), data.get("phoneNumber"), data.get("surname"))
        realtor.reviews = data.get("reviews")
        realtor.companyId = data.get("companyId")
        realtor.selfemployed = data.get("selfemployed")

        return realtor

if __name__ == "__main__":
    print(RealtorHelper.GetUniqueCode("sdfusgyfhisdfkjfdksf"))
    print(RealtorHelper.GetUniqueCode("sdfusgyfhisdfkjfdksfdkl;jfgdhsajfks"))
    print(len("sdfusgyfhisdfkjfdksfdkl;jfgdhsajfkslsdfkjghksdfhsl;kdslsfdj"))
    print(len(RealtorHelper.GetUniqueCode("sdfusgyfhisdfkjfdksfdkl;jfgdhsajfkslsdfkjghksdfhsl;kdslsfdj")))