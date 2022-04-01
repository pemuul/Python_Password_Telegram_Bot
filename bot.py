import telebot
import datetime
import os

import bot_setup
from bot_handler import Handler
from loging import Log_heandler
#from sqllite_main import Database

#import postgresql_main
from postgresql_main import Database

bot = telebot.TeleBot(os.environ.get('TOKEN'))
admin_id = int(os.environ.get('ADMIN_ID'))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	handler.send_welcome(message)

@bot.message_handler(commands=['add_password', 'get_password','delete_password'])
def help_comand(message):
	handler.send_welcome(message)


@bot.message_handler(commands=['add_colum'])
def get_log(message):
	if message.chat.id == admin_id:
		Database().add_colum('users_password', 'Create date', 'text')
		bot.send_message(message.chat.id, 'Ok')

@bot.message_handler(commands=['set_environ'])
def set_environ(message):
	if message.chat.id == admin_id:
		try:
			os.environ[message.text.split(' ')[1]] = message.text.split(' ')[2]
			bot.send_message(message.chat.id, 'Ok')
		except:
			bot.send_message(message.chat.id, 'Что-то не так')

@bot.message_handler(commands=['get_environ'])
def get_environ(message):
	if message.chat.id == admin_id:
		try:
			bot.send_message(message.chat.id, os.environ.get(message.text.split(' ')[1]))
		except:
			bot.send_message(message.chat.id, 'Что-то не так')

@bot.message_handler(commands=['test'])
def test(message):
	if message.chat.id == admin_id:
		#try:
			#print(os.environ.get('DATABASE_URL'))
		#text_l = message.text[len('/test') + 1:]
		#print(text_l)
		d = Database('db_sqlite.sqlite')
		#text_l = d.select(text_l)
		

		import sqlite3
		from postgresql_heandler import Table
 
		conn = sqlite3.connect("db_sqlite_to_dowland.sqlite")
		cursor = conn.cursor()

		for table_name in ['users', 'users_password']:
			text_l = d.select(f'SELECT * FROM {table_name}')
			Table_l = Table(table_name)
			for it in text_l:
				Table_l.insert(*it)
				#bot.send_message(message.chat.id, str(it))

			text_l = d.select(f'SELECT * FROM {table_name}')


		

		#os.remove("db_sqlite_to_dowland.sqlite")
		#except:
		#	bot.send_message(message.chat.id, 'Ошибка')

@bot.message_handler(commands=['get_log'])
def get_log(message):
	if message.chat.id == admin_id:
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
	if message.chat.id == admin_id:
		with open('db_sqlite.sqlite', 'r', encoding='utf-8') as log_file:
			bot.send_document(message.chat.id, log_file)

@bot.message_handler(commands=['get_file'])
def get_file(message):
	if message.chat.id == admin_id:
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
	if message.chat.id == admin_id:	
		bot.send_message(message.from_user.id, 'Доступ получен', reply_markup=handler.create_markup('admin'))


@bot.message_handler(content_types=['text'])
def get_text_messages2(message):
	handler.get_text_messages(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	handler.button_answer(call)


on_try = Database().project_in_server() # понимаем, где запущен код

while True:
	if on_try:
		try:
			handler = Handler(bot)
			handler.run_bot()
			Log_heandler().save_log('Бот был оставновлен')
		except Exception as e:
			Log_heandler().save_log(e)
	else:
		handler = Handler(bot)
		handler.run_bot()
		Log_heandler().save_log('Бот был оставновлен')


