class User:
    def __init__(self, chat_id, username, first_name, last_name, language_code, role='user'):
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code
        self.role = role

    @staticmethod
    def Deserialize(data: dict):
        user = User(data.get("chat_id"), data.get("username"), data.get("first_name"), data.get("last_name"), data.get('language_code'), data.get('role'))
        return user