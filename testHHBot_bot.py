import telebot
import user_history
import time
import os
import requests
import pprint
import time

TOKEN = 'токен'

bot=telebot.TeleBot(TOKEN)

#Пока стейт будем хранить в памяти, т.к. это учебный пример.
#Потом можно сделать сохранение в БД или файл.
chats = dict()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
"Это бот для работы с hh.ru
get_vacancies - Получить вакансии (первые 10 штук)
getstat - Получить статистику по вакансиям (файл с наиболее востребованными навыками и статистика по зарплате)
"\
""")

@bot.message_handler(commands=['get_vacancies', 'getstat'])
def start_dialog(message: object):
    if not message.chat.id in chats:
        #добавляем чат в список
        chat = user_history.UserState(message.chat.id)
        chats[message.chat.id] = chat

    chats[message.chat.id].command = message.text

    bot.send_message(message.chat.id, chats[message.chat.id].message_to_chat(message))





    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)

def echo_message(message):
    if not message.chat.id in chats:
        #добавляем чат в список
        chat = user_history.UserState(message.chat.id)
        chats[message.chat.id] = chat

    bot.send_message(message.chat.id, chats[message.chat.id].message_to_chat(message))






bot.infinity_polling()
