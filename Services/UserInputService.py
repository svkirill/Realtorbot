from telebot.types import Message
class UserInputService:
    """
    singleton - сервис, который создается при старте и живет бесконечно, одинаковый для всех пользователей
    scope - сервис, который создается новый каждый раз индивидуального для каждого вызова
    transient - сервис, который создается новый каждый раз индивидуального для каждого запроса
    """
    user_input = {}

    @staticmethod
    def process_data(message: Message, data_name):
        "{chatid: {...},chatid: {...},{...},{...}}"

        chatid = message.from_user.id
        data_value = message.text

        context = UserInputService.get_user_input(chatid)

        if context is None:
            context = {}
            UserInputService.user_input[chatid] = context

        context[data_name] = data_value

    @staticmethod
    def get_user_input(chatid):
        return UserInputService.user_input.get(chatid)