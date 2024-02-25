import json
import telebot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from Models.Realtor import Realtor

class MainService:
    bot = telebot.TeleBot('6939293439:AAGacBdkDXD-hBZ5sVHStGnkRrJ8tUyPWQY')
    user_data = {}
    user_input = {}
    addrealtortext = 'Добавить риелтора'
    realtors = []
    # key: chat_id, value : (key: data_name, value: data)

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_handler(message : Message):
        keyboard = ReplyKeyboardMarkup()
        button1 = KeyboardButton(text=MainService.addrealtortext)
        keyboard.add(button1)

        MainService.bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=keyboard)

    @staticmethod
    def process_data(chatid, data_name, data_value):
        "{chatid: {...},chatid: {...},{...},{...}}"

        context = MainService.user_input.get(chatid)

        if context is None:
            context = {}
            MainService.user_input[chatid] = context

        context[data_name] = data_value

    @staticmethod
    def process_realtor_data(chatid):
        context: dict = MainService.user_input.get(chatid)

        if context is not None:
            realtor = Realtor(context.get('name'), context.get('phonenumber'))
            MainService.realtors.append(realtor)
            MainService.SaveRealtorToJson(realtor)

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def start(message : Message):
        if message.text == MainService.addrealtortext:
            MainService.bot.send_message(message.from_user.id, "Введите номер телфона")
            MainService.bot.register_next_step_handler(message, MainService.get_name, key='phonenumber')

    @staticmethod
    def get_name(message : Message, key):
        data = message.text
        chatid = message.from_user.id
        MainService.process_data(chatid, key ,data)
        MainService.bot.send_message(chatid, "Введите имя риелтора")
        MainService.bot.register_next_step_handler(message, MainService.end_data_handler, key='name')

    @staticmethod
    def end_data_handler(message: Message, key):
        data = message.text
        chatid = message.from_user.id
        MainService.process_data(chatid, key, data)
        MainService.process_realtor_data(chatid)
        MainService.bot.send_message(chatid, f"Спасибо, данные сохранены.")

    @staticmethod
    def SaveRealtorToJson(realtor : Realtor):
        with open(f"Storage/realtor_{realtor.name}.json", 'w') as file:
            json.dump(realtor.__dict__, file)

    @staticmethod
    def LoadDataFromJson():
        with open("Storage/realtor.json", 'r') as file:
            data = json.load(file)
            return Realtor.Deserialize(data)

    @staticmethod
    def start():
        MainService.bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    MainService.start()
