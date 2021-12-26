from random import randint
from telethon import events, Button
from telethon.tl.custom import Message
from gen import bot
import sqlite3


markup = [Button.text('заявка', single_use=True, resize=True), Button.text('все заявки')]


conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(name_man: str, city_man: str, name_cus: str, target: str, kush: int, info: str):
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests(
        name_man CHAR   NOT NULL,
        city_man CHAR   NOT NULL,
        name_cus CHAR   NOT NULL,
        target   CHAR   NOT NULL,
        kush     CHAR   NOT NULL,
        info     STRING NOT NULL
        ); ''')
    cursor.execute('INSERT INTO requests (name_man, city_man, name_cus, target, kush, info) VALUES (?, ?, ?, ?, ?, ?)', (name_man, city_man, name_cus, target, kush, info))
    conn.commit()


def read_db():
    sqlite_select_query = """SELECT * from requests"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    cursor.close()
    return records


@bot.on(events.NewMessage(func=lambda event: event.text.lower() == 'привет'))
async def reload_command(event: Message):
    await event.respond('Привет! Ориентируйтесь по кнопкам ниже', buttons=markup)


@bot.on(events.NewMessage(func=lambda event: event.text.lower() == 'все заявки'))
async def all_offers(event):
    for row in read_db():
        await event.respond(f'''
                Заявка {randint(14, 140)}:

                Имя менеджера : {row[0][0] + '***'}    
                Город менеджера: {row[1]} 
                Имя клиента: {row[2]}
                Цель покупки: {row[3]}
                Бюджет: {row[4]}
                Дополнительная информация:{row[5]}
                ''')


@bot.on(events.NewMessage(func=lambda event: event.text.lower() == 'заявка'))
async def get_offer(event: Message):
    chat = await event.get_chat()

    async with bot.conversation(event.chat_id) as conv:
        
        await conv.send_message('Сейчас мы с Вамим по шагам создадим завку, это очень быстро и просто')
        await conv.send_message('Немного информации о Вас, напишите Ваше имя:')
        response = await conv.get_response()
        name_man = response.text
        await conv.send_message('Рады знакомству,{}!'.format(name_man))

        await conv.send_message('Из какого Вы города ?')
        response = await conv.get_response()
        city_man = response.text
        await conv.send_message('Отлично, теперь давайте перейдём к клиенту!')

        await conv.send_message(f'Скажите, {name_man}, как зовут Вашего клиента ?')
        response = await conv.get_response()
        name_cus = response.text
        
        await conv.send_message('Какая у него цель покупки ? (инвестиции или ПМЖ)')
        response = await conv.get_response()
        target = response.text

        await conv.send_message('Каков бюджет ?')
        response = await conv.get_response()
        kush = response.text

        await conv.send_message('Отлично, теперь напишите сопроводительную информацию (всё то, что считаете нужным')
        response = await conv.get_response()
        info = response.text

        await conv.send_message('Отлично! заявка сформирована и отправлена на модерацию')
        await conv.send_message(f'''
            Предварительный просмотр заявки:

            Имя менеджера : {name_man}
            Город менеджера: {city_man} 
            Имя клиента: {name_cus}
            Цель покупки: {target}
            Бюджет: {kush}
            Дополнительная информация:{info}
            ''', buttons=markup)
        
        db_table_val(name_man, city_man, name_cus, target, kush, info)
   

@bot.on(events.NewMessage(outgoing=False, pattern='hi'))
async def handler(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        await event.respond('Saved your photo {}'.format(sender.username))


@bot.on(events.NewMessage(pattern=r'(?i).*сука'))
async def handler1(event):
    await event.delete()
