import telebot
import config
from telebot import types
from action import Parsing_Post_Bot
import auth
from requests import get

bot = telebot.TeleBot(config.TOKEN)
last_action = ''

@bot.message_handler(commands=['start'])
def welcome(message):
    # Клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Скачать фото🌆")
    item2 = types.KeyboardButton("Перевести описание📝")
    markup.add(item1, item2)

    # Приветствие
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}! Что ты хочешь, чтобы я для тебя сделал?".format(message.from_user), parse_mode="html", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start_work(message):
    global last_action
    if message.chat.type == 'private':
        if message.text == 'Скачать фото🌆':
            last_action = 'Скачать фото🌆'
            bot.send_message(message.chat.id, "Отправь ссылку на пост")
    if message.chat.type == 'private':
        if message.text == 'Перевести описание📝':
            last_action = 'Перевести описание📝'
            bot.send_message(message.chat.id, "Отправь ссылку на пост")
    if message.chat.type == 'private':
        string = 'http'
        index = message.text.find(string)
        if index != -1 and last_action == 'Скачать фото🌆':
            my_bot = Parsing_Post_Bot(auth.username, auth.password)
            my_bot.login()
            downloaded = my_bot.download(message.text)
            for item in downloaded:
                try:
                    bot.send_photo(message.chat.id, get(item).content)
                except:
                    bot.send_video(message.chat.id, get(item).content)
            last_action = ''
    if message.chat.type == 'private':
        string = 'http'
        index = message.text.find(string)
        if index != -1 and last_action == 'Перевести описание📝':
            my_bot = Parsing_Post_Bot(auth.username, auth.password)
            my_bot.login()
            bot.send_message(message.chat.id, my_bot.descriotion(message.text))
            last_action = ''

bot.polling(none_stop=True)