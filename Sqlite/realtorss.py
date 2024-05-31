from peewee import *
connection = SqliteDatabase("storage.db")
class Realtor(Model):
    id = AutoField(column_name="Id", null=False, primary_key=True)
    name = TextField(column_name='Name', null=False)
    surname = TextField(column_name='Surname', null=False)
    companyId = IntegerField(column_name='CompanyId')  # FK
    selfemployed = BooleanField(column_name='SelfEmployed', default=True)

    class Meta:
        """
        Класс метаданных - любые данные, которые не касаются основных данных,
        данные для данных.
        """
        table_name = "realtors"
        database = connection
Realtor.create_table()

class User(Model):
    chat_id = IntegerField(column_name='ChatId', null=False, primary_key=True)
    username = TextField(column_name='Username', null=True)
    first_name = TextField(column_name='Firstname', null=True)
    last_name = TextField(column_name='Lastname', null=True)
    language_code = TextField(column_name='LanguageCode', null=True)
    role = TextField(column_name='Role', default='user', null=False)

    class Meta:
        table_name = 'users'
        database = connection
User.create_table()


class Company(Model):
    id = AutoField(column_name='Id', primary_key=True)
    name = TextField(column_name='CompanyName')
    phonenumber = TextField(column_name='CompanyPhoneNumber')

    class Meta:
        table_name = 'company'
        database = connection
Company.create_table()

connection.close()
