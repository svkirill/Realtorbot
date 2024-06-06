from peewee import *
connection = SqliteDatabase("storage.db")

USER_ROLE_ID = 1
ADMIN_ROLE_ID = 2

USER_ROLE_NAME = "user"
ADMIN_ROLE_NAME = "admin"

class Company(Model):
    id = AutoField(column_name='Id', primary_key=True)
    name = TextField(column_name='CompanyName')
    phonenumber = TextField(column_name='CompanyPhoneNumber')

    class Meta:
        table_name = 'company'
        database = connection
Company.create_table()

class Realtor(Model):
    id = AutoField(column_name="Id", null=False, primary_key=True)
    name = TextField(column_name='Name', null=False)
    surname = TextField(column_name='Surname', null=False)
    company = ForeignKeyField(Company, column_name='CompanyId', related_name="realtors")  # FK
    selfemployed = BooleanField(column_name='SelfEmployed', default=True)

    class Meta:
        """
        Класс метаданных - любые данные, которые не касаются основных данных,
        данные для данных.
        """
        table_name = "realtors"
        database = connection
Realtor.create_table()


class Role(Model):
    id = IntegerField(column_name="Id", null=False, primary_key=True)
    name = TextField(column_name="Name", null=False)

    class Meta:
        table_name = 'roles'

        database = connection

Role.create_table()

def find_role(id):
    for role in Role.select():
        if role.id == id:
            return True
    return False

if not find_role(USER_ROLE_ID):
    Role.create(id=USER_ROLE_ID, name=USER_ROLE_NAME)

if not find_role(ADMIN_ROLE_ID):
    Role.create(id=ADMIN_ROLE_ID, name=ADMIN_ROLE_NAME)

class User(Model):
    chat_id = IntegerField(column_name='ChatId', null=False, primary_key=True)
    username = TextField(column_name='Username', null=True)
    first_name = TextField(column_name='Firstname', null=True)
    last_name = TextField(column_name='Lastname', null=True)
    language_code = TextField(column_name='LanguageCode', null=True)
    role = ForeignKeyField(Role, column_name='RoleId', default=USER_ROLE_ID, related_name="users")

    class Meta:
        table_name = 'users'

        database = connection
User.create_table()





if __name__ == "__main__":
    company = Company.create(name="OOO TEST", phonenumber="2138231")
    realtor = Realtor.create(name="test", surname="test", company=company) # create - автоматически сохраняет в БД, тебе не надо вызывать save
    realtor2 = Realtor.create(name="test2", surname="test2", company=company.id) # можно передавать в FK как и PK так и полноценный объект
    print(realtor.company.name)
    for realtor in company.realtors:
        print(realtor.name)

    user = User.create(chat_id=128192,username="test", first_name="sdfs", last_name="sdfsd", language_code="ru")

    print("")

connection.close()

