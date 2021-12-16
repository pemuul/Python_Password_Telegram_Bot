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
	if message.chat.id == bot_setup.ADMIN_ID:
		text = message.text.split(' ')
		if len(text) < 2:
			log_name = Log_heandler().get_log_name_file()
		else:
			log_name = Log_heandler().get_log_name_file(now_P = text[1])
		try:
			with open(log_name, 'r') as log_file:
				bot.send_document(message.chat.id, log_file)
		except:
			bot.send_message(message.chat.id, 'Такого файла нет!')

@bot.message_handler(commands=['get_db'])
def get_db(message):
	if message.chat.id == bot_setup.ADMIN_ID:
		with open('db_sqlite.sqlite', 'r', encoding='utf-8') as log_file:
			bot.send_document(message.chat.id, log_file)

@bot.message_handler(commands=['get_file'])
def get_file(message):
	if message.chat.id == bot_setup.ADMIN_ID:
		text = message.text.split(' ')
		if len(text) < 2:
			bot.send_message(message.chat.id, 'Введите имя файла')
			return ()
		try:
			with open(text[1], 'r') as log_file:
				bot.send_document(message.chat.id, log_file)
		except:
			bot.send_message(message.chat.id, 'Ошибка')

@bot.message_handler(commands=['admin'])
def admin(message):
	if message.chat.id == bot_setup.ADMIN_ID:	
		bot.send_message(message.from_user.id, 'Доступ получен', reply_markup=handler.create_markup('admin'))


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
