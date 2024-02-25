class Realtor:
    def __init__(self,name, phoneNumber, surname=""):
        self.name = name
        self.phoneNumber = phoneNumber
        self.surname = surname
        self.reviews = []   # TODO - возможно нужно завести класс
        self.companyId = 0
        self.selfemployed = True

    @staticmethod
    def Deserialize(data : dict):
        realtor = Realtor(data.get("name"), data.get("phoneNumber"), data.get("surname"))
        realtor.reviews = data.get("reviews")
        realtor.companyId = data.get("companyId")
        realtor.selfemployed = data.get("selfemployed")

        return realtor