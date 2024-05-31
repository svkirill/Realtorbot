from Models.Company import Company
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os.path
class CompanyService:
    companies = []
    storagePath = 'Storage/company.json'
    DEFAULT_PAGE_SIZE = 5
    NOT_VISIBLE_SYMBOL = "ㅤ"
    NEXT_TEXT = "Далее👉"
    BACK_TEXT = "👈Назад"

    @staticmethod
    def FindCompanyById(id):
        for company in CompanyService.companies:
            if company.id == id:
                return company
        return None

    @staticmethod
    def get_companies_menu(pageNumber, pageSize=None):
        if pageSize is None:
            pageSize = CompanyService.DEFAULT_PAGE_SIZE

        keyboard = InlineKeyboardMarkup()
        endIndex = pageNumber * pageSize - 1
        startIndex = endIndex - (pageSize - 1)
        for company in CompanyService.companies[startIndex:endIndex + 1]:
            text = company.name
            button = InlineKeyboardButton(text=text, callback_data=f"CompanyId_{company.id}")
            keyboard.add(button)

        # Добавляем кнопку далее, если это необходимо
        nextText = CompanyService.NEXT_TEXT
        if endIndex >= len(CompanyService.companies) - 1:
            nextText = CompanyService.NOT_VISIBLE_SYMBOL

        btn_next = InlineKeyboardButton(text=nextText, callback_data=f"PageNum_{pageNumber+1}")

        # Добавляем кнопку назад, если это необходимо
        backText = CompanyService.BACK_TEXT
        if pageNumber <= 1:
            backText = CompanyService.NOT_VISIBLE_SYMBOL

        btn_back = InlineKeyboardButton(text=backText, callback_data=f"PageNum_{pageNumber-1}")

        keyboard.add(btn_back, btn_next)

        return keyboard

    @staticmethod  # TODO - бд
    def SaveCompanyToJson():
        company = []
        saveCompany = {"objects": company}

        for company in CompanyService.company:
            company.append(company.__dict__)


        with open(CompanyService.storagePath, 'w') as file:
            json.dump(saveCompany, file)


    @staticmethod  # TODO - бд
    def LoadDataFromJson():
        if os.path.exists(CompanyService.storagePath):
            with open(CompanyService.storagePath, 'r') as file:
                data = json.load(file)

                company = data.get("objects", [])  # [] - default value
                result = []

                for companyDict in company:
                    result.append(Company.Deserialize(companyDict))

                return result
        return []

    @staticmethod
    def InitData():
        CompanyService.companies = CompanyService.LoadDataFromJson()

if __name__ == "__main__":
    CompanyService.storagePath = "../Storage/company.json"

    data = CompanyService.InitData()
    print(CompanyService.companies)

    print(CompanyService.companies[0])