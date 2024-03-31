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
    backmenu = 'Вернуться в главное меню'

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_handler(message : Message):
        user = UserService.GetUserByContext(message)

        MainService.send_start_keyboard(user, "Добро пожаловать!")

    @staticmethod
    def send_start_keyboard(user, message):

        keyboard = ReplyKeyboardMarkup()
        button1 = KeyboardButton(text=MainService.addrealtortext)
        button2 = KeyboardButton(text=MainService.showrealtors)
        keyboard.add(button1)
        keyboard.add(button2)

        MainService.bot.send_message(user.chat_id, message, reply_markup=keyboard)


    @staticmethod
    @bot.message_handler(content_types=['text'])
    def start(message : Message):
        user = UserService.GetUserByContext(message)

        if message.text == MainService.addrealtortext:

            MainService.bot.send_message(message.chat.id, "Введите номер телeфона")
            MainService.bot.register_next_step_handler(message, MainService.get_name, key='phonenumber')
        elif message.text == MainService.showrealtors or message.text == RealtorsService.BACK_TEXT or message.text == RealtorsService.NEXT_TEXT:
            page = 1
            if message.text == RealtorsService.NEXT_TEXT:
                page = UserPagesRememberService.NextPageInvoked(message.chat.id)
            elif message.text == RealtorsService.BACK_TEXT:
                page = UserPagesRememberService.BackPageInvoked(message.chat.id)

            MainService.bot.send_message(message.from_user.id,"Смотрите в меню ниже.", reply_markup=RealtorsService.get_realtors_menu(page))

        elif message.text == RealtorsService.backmenuu:
            MainService.send_start_keyboard(user, "Главное меню")


    @staticmethod   # TODO - вынесение в класс пользовательского ввода
    def get_name(message : Message, key):
        user = UserService.GetUserByContext(message.chat.id)

        UserInputService.process_data(message, key)

        MainService.bot.send_message(message.from_user.id, "Введите имя риелтора")
        MainService.bot.register_next_step_handler(message, MainService.end_data_handler, key='name')

    @staticmethod   # TODO - вынесение в класс пользовательского ввода
    def end_data_handler(message: Message, key):
        user = UserService.GetUserByContext(message.chat.id)

        UserInputService.process_data(message, key)

        RealtorsService.process_realtor_data(message.from_user.id)
        MainService.bot.send_message(message.from_user.id, f"Спасибо, данные сохранены.")

    @staticmethod
    def start():
        RealtorsService.InitData()
        UserService.InitData()

        for user in UserService.users:
            MainService.send_start_keyboard(user, "Продолжаем работу...")

        MainService.bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    MainService.start()
