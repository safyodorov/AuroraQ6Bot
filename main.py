from get_image import getImage
from get_q_index import getQ
from psql import get_user, id_check, id_write
import os
import telebot
import threading
import schedule
import time

aurora = {'5': '. Cияние видно на широте 62° (г. Петрозаводск).',
          '6': '. Сияние видно на широте 60° (г. Санкт-Петербург).',
          '7': '. Сияние видно на широте 56° (Иваново, Москва, Нижний Новгород, Казань, Екатеринбург, Новосибирск).',
          '8': '. Сияние видно на широте 52° (Самара, Курск, Липецк).',
          '9': '. Сияние видно на широте 50°–45° (Крым, Кавказ).'}

# клавиатура telegram вывел отдельно
def keyboard():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Узнать Q-индекс', callback_data="index"))
    markup.add(telebot.types.InlineKeyboardButton(text='Получить график', callback_data="picture"))
    markup.add(telebot.types.InlineKeyboardButton(text='Настроить уведомления', callback_data="notifications"))
    markup.add(telebot.types.InlineKeyboardButton(text='About', callback_data="about"))
    return markup

def keyboardnotes():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Не получать уведомления', callback_data='0'))
    for i in range(5, 10):
        markup.add(telebot.types.InlineKeyboardButton(text='Сообщать когда Q-индекс >='+i, callback_data=i))
    markup.add(telebot.types.InlineKeyboardButton(text='About', callback_data="about"))
    return markup

# telegram bot
BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN)

joinedUser5, joinedUser6, joinedUser7, joinedUser8, joinedUser9 = get_user()

@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    username = message.from_user.username

    id_check(id, username)

    markup = keyboard()
    bot.send_message(message.chat.id, text="Привет, чем могу помочь?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    id = call.message.chat.id
    if call.data == "index":
        Q = getQ()
        bot.send_message(call.message.chat.id, "Привет, Q-индекс: "+str(Q))
    elif call.data == "picture":
        getImage()
        bot.send_photo(call.message.chat.id, open('Q-index.png', 'rb'))
    elif call.data == "about":
        bot.send_message(call.message.chat.id, 'AuroraQIBot v.1\n'
                                               '\n'
                                               'Бот получает онлайн-данные с магнитометров, расположенных в городе Кируна (Швеция)\n'
                                               'сайт: https://www2.irf.se/Observatory/?link[Magnetometers]=Data/\n'
                                               '\n'
                                               'Бот позволяет по запросу получить:\n'
                                               '– актуальное значение Q-индекса;\n'
                                               '– график изменения Q-индекса за последние сутки.\n'
                                               '\n'
                                               'Главная особенность этого бота:\n'
                                               'настраиваемые уведомления пользователей о значениях Q-индекса.')

    elif call.data == "notifications":
        markup = keyboardnotes()
        bot.send_message(call.message.chat.id, "Хорошо", reply_markup=markup)
    else:
        data = call.data
        id_write(id, data)
        if data == '0':
            bot.send_message(call.message.chat.id, 'Уведомления отключены')
        else:
            bot.send_message(call.message.chat.id, 'Буду присылать уведомления, когда Q-индекс будет >=' + data + aurora[data])

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    if message.text == "ку" or message.text == "Ку" or message.text == "КУ" or message.text == "кУ":
        Q = getQ()
        bot.send_message(message.chat.id, "Привет, Q-индекс: "+str(Q))
    elif message.text == "график" or message.text == "График" or message.text == "ГРАФИК" or message.text == "гРАФИК":
        getImage()
        bot.send_photo(message.chat.id, open('Q-index.png', 'rb'))
    else:
        markup = keyboard()
        bot.send_message(message.chat.id, "Напишите: ку ИЛИ график. ИЛИ нажмите на кнопку ", reply_markup=markup)

# функция проверяет значения индекса Q и присылает уведомления в зависимости от выбора пользователя
def AuroraPossible(joinedUser5,joinedUser6, joinedUser7, joinedUser8, joinedUser9):
    Q = getQ()
    if Q >= 2:
        if joinedUser5:
            for user in joinedUser5:
                bot.send_message(user, "Внимание значение Q велико, возможно Северное сияние. Q-индекс: "+str(Q))
    elif Q >= 3:
        if joinedUser6:
            for user in joinedUser6:
                bot.send_message(user, "Внимание значение Q велико, возможно Северное сияние. Q-индекс: "+str(Q))
    elif Q >= 7:
        if joinedUser7:
            for user in joinedUser7:
                bot.send_message(user, "Внимание значение Q велико, возможно Северное сияние. Q-индекс: "+str(Q))
    elif Q >= 8:
        if joinedUser8:
            for user in joinedUser8:
                bot.send_message(user, "Внимание значение Q велико, возможно Северное сияние. Q-индекс: "+str(Q))
    elif Q >= 9:
        if joinedUser9:
            for user in joinedUser9:
                bot.send_message(user, "Внимание значение Q велико, возможно Северное сияние. Q-индекс: "+str(Q))

# уведомления
def notifications(joinedUser5, joinedUser6, joinedUser7, joinedUser8, joinedUser9):
    schedule.every(15).minutes.do(AuroraPossible, joinedUser5, joinedUser6, joinedUser7, joinedUser8, joinedUser9)

    while True:
        schedule.run_pending()
        time.sleep(1)  # сейчас интервал 1 секунда

if __name__ == '__main__':
    t1 = threading.Thread(target=bot.polling)
    t2 = threading.Thread(target=notifications, args=(joinedUser5, joinedUser6, joinedUser7, joinedUser8, joinedUser9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()