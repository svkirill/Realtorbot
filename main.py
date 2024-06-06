import json
import telebot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from Services.UserInputService import UserInputService
from Services.RealtorsService import RealtorsService
from Services.UserPagesRememberService import UserPagesRememberService
from Services.UserService import UserService
from Services.CompanyService import CompanyService
import os.path
from Models.Realtor import  RealtorHelper
class MainService:
    bot = telebot.TeleBot('6939293439:AAGacBdkDXD-hBZ5sVHStGnkRrJ8tUyPWQY')
    addrealtortext = 'Добавить риелтора'    # TODO - вынесение
    showrealtors = "Список риелторов"
    backmenu = 'Вернуться в главное меню'
    adminbutton = 'Скачать базу пользователей'

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_handler(message : Message):
        user = UserService.GetUserByContext(message)

        MainService.send_start_keyboard(user, "👋Добро пожаловать!👋")

    @staticmethod
    def send_start_keyboard(user, message):

        keyboard = ReplyKeyboardMarkup()
        button1 = KeyboardButton(text=MainService.addrealtortext)
        button2 = KeyboardButton(text=MainService.showrealtors)
        keyboard.add(button1)
        keyboard.add(button2)

        if user.role.name == 'admin':
            button3 = KeyboardButton(text=MainService.adminbutton)
            keyboard.add(button3)

        #MainService.bot.send_document(chat_id, считанный файл, название)
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
            else:
                UserPagesRememberService.UserGetRealtorsList(user.chat_id)
            MainService.bot.send_message(message.from_user.id,"👇Смотрите в меню ниже.👇", reply_markup=RealtorsService.get_realtors_menu(page))

        elif message.text == RealtorsService.backmenuu:
            MainService.send_start_keyboard(user, "Главное меню")

        elif message.text == MainService.adminbutton:
            if user.role.name == 'admin':
                MainService.SendDataBaseToUser(user.chat_id, [RealtorsService.storagePath, UserService.storagePath])
        else:
            realtorInfo = RealtorsService.GetRealtorInfo(message.text)
            if realtorInfo != None:
                # create keyboard
                keyboard = InlineKeyboardMarkup()
                uniqueCode = RealtorHelper.GetUniqueCode(message.text)
                button1 = InlineKeyboardButton(text='-Оставить отзыв-', callback_data=f'SendReview_{uniqueCode}')
                button2 = InlineKeyboardButton(text='-Изменить информацию-', callback_data=f'ChangeInfo_{uniqueCode}')
                button3 = InlineKeyboardButton(text='-Посмотреть отзывы-', callback_data=f'Reviews_{uniqueCode}')
                keyboard.add(button1)
                keyboard.add(button2)
                keyboard.add(button3)

                MainService.bot.send_message(user.chat_id, realtorInfo, reply_markup=keyboard)
            else:
                MainService.bot.send_message(user.chat_id,"😐Я вас не понимаю😐")

    func_to_question = {
        RealtorsService.CHANGE_NAME_PARAM: "Введите новое имя...",
        RealtorsService.CHANGE_SURNAME_PARAM: "Введите новую фамилию...",
        RealtorsService.CHANGE_PHONENUMBER_PARAM: 'Введите новый номер телефона...',
        RealtorsService.CHANGE_SELFEMPLOYED_PARAM: '',
        RealtorsService.CHANGE_COMPANY_PARAM: "Chose company...",
        "PageNum": "Chose company..."
    }

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    def pressed_handler(call):
        user = UserService.GetUserByContext(call.message)

        splitedData = call.data.split("_")
        func = splitedData[0]
        uniqueCode = splitedData[1]
        print(func)
        if func == "SendReview":
            m_id = call.message.message_id
            id = call.message.chat.id
            MainService.bot.edit_message_text(chat_id=id,  message_id=m_id, text='Напишите отзыв')
            #MainService.bot.send_message(user.chat_id, "Напишите отзыв")
            MainService.bot.register_next_step_handler(call.message, MainService.save_review_handler, uniqueCode=uniqueCode)
        elif func == "ChangeInfo":
            m_id = call.message.message_id
            id = call.message.chat.id
            keyboard = InlineKeyboardMarkup()
            button1 = InlineKeyboardButton(text='Имя', callback_data=f'{RealtorsService.CHANGE_NAME_PARAM}_{uniqueCode}')
            button2 = InlineKeyboardButton(text='Фамилия', callback_data=f'ChangeSurname_{uniqueCode}' )
            button3 = InlineKeyboardButton(text='Номер телефона', callback_data=f'ChangePhoneNumber_{uniqueCode}')
            button4 = InlineKeyboardButton(text='Company', callback_data=f'ChangeCompany_{uniqueCode}')
            print(len(f'ChangePhoneNumber_{uniqueCode}'.encode('utf-8')))
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)
            print(keyboard)
            MainService.bot.edit_message_text(chat_id=id,  message_id=m_id, text="Что вы хотите изменить?", reply_markup=keyboard)
        elif func == "PageNum" or func == RealtorsService.CHANGE_NAME_PARAM or func == RealtorsService.CHANGE_SURNAME_PARAM or func == RealtorsService.CHANGE_PHONENUMBER_PARAM or func == RealtorsService.CHANGE_COMPANY_PARAM:
            m_id = call.message.message_id
            id = call.message.chat.id

            replyMarkup = None

            if func == RealtorsService.CHANGE_COMPANY_PARAM:
                replyMarkup = CompanyService.get_companies_menu(1)
                print(replyMarkup)

            if func == "PageNum":
                print(int(uniqueCode))
                replyMarkup = CompanyService.get_companies_menu(int(uniqueCode))
                print(replyMarkup)

            MainService.bot.edit_message_text(chat_id=id,  message_id=m_id, text= MainService.func_to_question.get(func), reply_markup=replyMarkup)
            MainService.bot.register_next_step_handler(call.message, MainService.change_info_handler, callback_data=call.data)
        elif func == "Reviews":
            m_id = call.message.message_id
            id = call.message.chat.id

            text = "Отзывы о риэлторе:\n"

            realtor = RealtorsService.FindbyCode(uniqueCode)

            if realtor is not None:
                if len(realtor.reviews) == 0:
                    text = "Отзывов нет."

                for review in realtor.reviews:
                    text += f"- {review}\n"

                MainService.bot.edit_message_text(chat_id=id,  message_id=m_id, text=text)



    @staticmethod
    def SendDataBaseToUser(chat_id, paths:list):
        for path in paths:
            if os.path.exists(path):
                with open(path, 'rb') as file:
                    MainService.bot.send_document(chat_id, file)

    @staticmethod   # TODO - вынесение в класс пользовательского ввода
    def get_name(message : Message, key):
        user = UserService.GetUserByContext(message)

        UserInputService.process_data(message, key)

        MainService.bot.send_message(message.from_user.id, "Введите имя риелтора")
        MainService.bot.register_next_step_handler(message, MainService.end_data_handler, key='name')

    @staticmethod  # TODO - вынесение в класс пользовательского ввода
    def save_review_handler(message: Message, uniqueCode):
        user = UserService.GetUserByContext(message)

        # код обработки отзыва из message.text и сохранение его в риэлтора, которого ты найдешь по uniqueCode
        review = message.text
        result = RealtorsService.AddReviewToRealtor(review, uniqueCode)

        if result:
            MainService.bot.send_message(user.chat_id, "🤝Спасибо за отзыв!🤝")
        else:
            MainService.bot.send_message(user.chat_id, "Произошла ошибка.")

    @staticmethod  # TODO - вынесение в класс пользовательского ввода
    def change_info_handler(message: Message, callback_data):
        user = UserService.GetUserByContext(message)

        data = message.text
        splitedData = callback_data.split("_")
        func = splitedData[0]
        uniqueCode = splitedData[1]
        print(f"Old unique code: {uniqueCode}")
        # Поменять параметр риэлтора
        if user.role.name == "admin":
            uniqueCode = RealtorsService.ChangeRaltorParam(uniqueCode, func, data)
            print(f"New unique code: {uniqueCode}")
            MainService.bot.send_message(user.chat_id, 'Данные изменены.')

            chatIds_to_resend_keyboard = UserPagesRememberService.CheckResendChangedPages(uniqueCode)
            MainService.ResendKeyBoardForUsers(chatIds_to_resend_keyboard)
        else:
            MainService.bot.send_message(user.chat_id, 'Ваши изменения на проверке')

    @staticmethod
    def ResendKeyBoardForUsers(chat_ids:list):
        for chat_id in chat_ids:
            MainService.bot.send_message(chat_id, "Данные риэлторов на вашей странице были обновлены. Новая клавиатура ниже.",
                                         reply_markup=RealtorsService.get_realtors_menu(UserPagesRememberService.GetCurrentUserPage(chat_id)))


    @staticmethod   # TODO - вынесение в класс пользовательского ввода
    def end_data_handler(message: Message, key):
        user = UserService.GetUserByContext(message)

        UserInputService.process_data(message, key)
        RealtorsService.process_realtor_data(message.from_user.id)
        MainService.bot.send_message(message.from_user.id, f"Спасибо, данные сохранены.")

    @staticmethod
    def start():
        RealtorsService.InitData()
        #UserService.InitData()
        CompanyService.InitData()

        for user in UserService.GetUsers():
            MainService.send_start_keyboard(user, "Продолжаем работу...")

        MainService.bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    MainService.start()
