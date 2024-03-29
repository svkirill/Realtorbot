import json
import telebot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from Services.UserInputService import UserInputService
from Services.RealtorsService import RealtorsService
from Services.UserPagesRememberService import UserPagesRememberService
from Services.UserService import UserService
class MainService:
    bot = telebot.TeleBot('6939293439:AAGacBdkDXD-hBZ5sVHStGnkRrJ8tUyPWQY')
    addrealtortext = 'Добавить риелтора'    # TODO - вынесение
    showrealtors = "Список риелторов"

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_handler(message : Message):
        user = UserService.GetUser(message.chat.id)

        MainService.send_start_keyboard(user)

    @staticmethod
    def send_start_keyboard(user):
        keyboard = ReplyKeyboardMarkup()
        button1 = KeyboardButton(text=MainService.addrealtortext)
        button2 = KeyboardButton(text=MainService.showrealtors)
        keyboard.add(button1)
        keyboard.add(button2)

        MainService.bot.send_message(user.chat_id, "Добро пожаловать!", reply_markup=keyboard)


    @staticmethod
    @bot.message_handler(content_types=['text'])
    def start(message : Message):
        user = UserService.GetUser(message.chat.id)

        if message.text == MainService.addrealtortext:
            MainService.bot.send_message(user.chat_id, "Введите номер телфона")
            MainService.bot.register_next_step_handler(message, MainService.get_name, key='phonenumber')
        elif message.text == MainService.showrealtors or message.text == RealtorsService.BACK_TEXT or message.text == RealtorsService.NEXT_TEXT:

            page = 1
            if message.text == RealtorsService.NEXT_TEXT:
                page = UserPagesRememberService.NextPageInvoked(message.chat.id)
            elif message.text == RealtorsService.BACK_TEXT:
                page = UserPagesRememberService.BackPageInvoked(message.chat.id)

            MainService.bot.send_message(message.from_user.id,"Смотрите в меню ниже.", reply_markup=RealtorsService.get_realtors_menu(page))


    @staticmethod   # TODO - вынесение в класс пользовательского ввода
    def get_name(message : Message, key):
        user = UserService.GetUser(message.chat.id)

        UserInputService.process_data(message, key)

        MainService.bot.send_message(message.from_user.id, "Введите имя риелтора")
        MainService.bot.register_next_step_handler(message, MainService.end_data_handler, key='name')

    @staticmethod   # TODO - вынесение в класс пользовательского ввода
    def end_data_handler(message: Message, key):
        user = UserService.GetUser(message.chat.id)

        UserInputService.process_data(message, key)

        RealtorsService.process_realtor_data(message.from_user.id)
        MainService.bot.send_message(message.from_user.id, f"Спасибо, данные сохранены.")

    @staticmethod
    def start():
        RealtorsService.InitData()
        UserService.InitData()

        for user in UserService.users:
            MainService.send_start_keyboard(user)

        MainService.bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    MainService.start()
