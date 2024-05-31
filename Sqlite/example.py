from peewee import *
# ORM - Object Relation Mapping
from uuid import uuid4

connection = SqliteDatabase("users.db")

class Users(Model):
    user_id = AutoField(column_name="id")
    username = TextField(null=False)
    name = TextField(null=True)
    surname = TextField(null=True)

    class Meta:
        """
        Класс метаданных - любые данные, которые не касаются основных данных,
        данные для данных.
        """
        table_name = "users"
        database = connection

Users.create_table()


#user = Users(username = "TestUser")
#print(user.username)
#user.save()

#user2 = Users.create(username="TestUser2")
#user2.save()

user = Users.get(Users.user_id == 1)
print(user.username)

for user in Users.select():
    print(f"{user.user_id}. {user.username}")

connection.close()
