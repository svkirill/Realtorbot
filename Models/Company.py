from uuid import uuid4
class Company:
    def __init__(self, name, phonenumber, reviews, id=None):
        self.name = name
        self.phonenumber = phonenumber
        self.reviews = reviews

        if id is None:
            id = str(uuid4())

        self.id = id

    def __str__(self):
        return f"{self.id} - {self.name}"

    @staticmethod
    def Deserialize(data: dict):
        company = Company(data.get("name"), data.get("phonenumber"), data.get("reviews"), data.get("id"))
        return company