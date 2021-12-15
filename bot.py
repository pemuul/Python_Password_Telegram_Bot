import telebot
import datetime

import bot_setup
from bot_handler import Handler
from loging import Log_heandler
from sqllite_main import Database

bot = telebot.TeleBot(bot_setup.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	handler.send_welcome(message)

@bot.message_handler(commands=['add_colum'])
def get_log(message):
	if message.chat.id == bot_setup.ADMIN_ID:
		Database().add_colum('users_password', 'Create date', 'text')
		bot.send_message(message.chat.id, 'Ok')

@bot.message_handler(commands=['get_log'])
def get_log(message):
	bot.send_message(message.chat.id, str(Log_heandler().get_tooday_log()))

@bot.message_handler(content_types=['text'])
def get_text_messages2(message):
	handler.get_text_messages(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	handler.button_answer(call)
	

while True:
	try:
		handler = Handler(bot)
		handler.run_bot()
		Log_heandler().save_log('Бот был оставновлен')
	except Exception as e:
		Log_heandler().save_log(e)
