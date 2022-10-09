from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3

TOKEN = os.environ['token']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
users = {}

def create_users():
    connect = sqlite3.connect('usersBot_data_base.db')
    cursor = connect.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                   "UserId TEXT, "
                   "First_name TEXT, "
                   "Phone TEXT, "
                   "Address TEXT, "
                   "email TEXT,"
                  )
    connect.commit()
    cursor.close()
    create_users()


def get_users(id_user):
    connect = sqlite3.connect('usersBot_data_base.db')
    cursor = connect.cursor()
    get = f'SELECT * FROM users WHERE UserId="{id_user}"'
    user = cursor.execute(get).fetchall()
    connect.commit()
    cursor.close()
    return user

def add_user(id_user, text_message):
    connect = sqlite3.connect('usersBot_data_base.db')
    cursor = connect.cursor()
    get = f"UPDATE users SET 'Text_massage' = {text_message} WHERE UserId = {id_user}"
    cursor.execute(get)
    connect.commit()
    cursor.close()

def insert_user(user:dict):
    connect = sqlite3.connect('usersBot_data_base.db')
    cursor = connect.cursor()
    get = f'INSERT INTO users(UserId, First_name, Phone, Address, email)' \
          f' VALUES' \
          f' ("{user["UserId"]},' \
          f' "{str(user["First_name"])}",' \
          f' "{str(user["Phone"])}",' \
          f' "{str(user["Address"])}",' \
          f'"{str(user["email"])}",' \
          f')'
    cursor.execute(get)
    connect.commit()
    cursor.close()


@dp.message_handler()
async def recording(message: types.Message):
    print(message.from_user.id, ' - ', message.from_user.first_name, ' - ', message.text)


    users.update({message.from_user.id: message.from_user.first_name})
    #await message.answer(message.text)
    #await message.reply(message.text)
    text = f'Пользователь {message.from_user.first_name} написал {message.text}'
    for i in users.keys():
        if i != message.from_user.id:
            await bot.send_message(chat_id=i, text=text)


if __name__ == '__main__':
    executor.start_polling(dp)