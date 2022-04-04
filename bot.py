import telebot
import datetime
import os

import bot_setup
from bot_handler import Handler
from loging import Log_heandler
#from sqllite_main import Database

#import postgresql_main
from postgresql_main import Database, Database_Mgt

bot = telebot.TeleBot(os.environ.get('TOKEN'))
admin_id = int(os.environ.get('ADMIN_ID'))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	handler.send_welcome(message)

@bot.message_handler(commands=['add_password', 'get_password','delete_password'])
def help_comand(message):
	# при вводе вспомогательной команды 
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
		d = Database('db_sqlite.sqlite')
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
			bot.send_message(message.chat.id, 'Логов нет!')

@bot.message_handler(commands=['get_db'])
def get_db(message):
	# создаём SQLLite файл, переливаем в него все данные и отправляем 
	'''
	if message.chat.id == admin_id:
		import psycopg2
		import sys
		import sqlite3

		connection = None

		#try:
		connection = Database('db_sqlite.sqlite').connection
		connection_backup = sqlite3.connect('beckup.sqlite')
		connection.backup(connection_backup, pages=0, progress=None, name="main", sleep=0.250)
		connection_backup.close()

		with open('beckup.sqlite', 'r') as log_file:
			bot.send_document(message.chat.id, log_file)
		#except:
		#	bot.send_message(message.chat.id, 'Не вышло:(')

		os.remove('beckup.sqlite')
	'''
	import sqlite3
	import json
	from postgresql_heandler import Table
	# создать новую базу SQLite
	beckup_db_name = 'beckup.sqlite'
	connection_backup = sqlite3.connect(beckup_db_name)
	
	#print(f'{message.chat.id}: Начал сборку данных')
	Log_heandler().save_log(f'{message.chat.id}: Начал сборку данных')
	bot.send_message(message.chat.id, 'Сборка данный начата!')

	# получить все таблицы и через цикл создать их в новой базе
	with open("shem_table.json", "r", encoding='utf-8') as read_file:
		shem_json = json.load(read_file)
		print(shem_json.keys())
	for table_name in shem_json:
		#print(table_name)
		table_becup = Table(table_name, beckup_db_name, False)
		table_main = Table(table_name)
		db_becup = table_becup.db
		cursor_becup = db_becup.cur
		#print([i[0] for i in table.get_all()])
		for data in table_main.get_all():
			#
			data = [str(d) for d in data]
			data_set = "', '".join(data)
			#print(shem_json[table_name]['always_fild'])
			line_name = '", "'.join(shem_json[table_name]['always_fild'])
			line_name = f'"{line_name}"'
			#print(line_name)
			#print(f"INSERT INTO {table_name} ({line_name}) VALUES('{data_set}')")
			cursor_becup.execute(f"INSERT INTO {table_name} ({line_name}) VALUES('{data_set}')")

		#print(table_becup.get_all())
		db_becup.close()
	# запросами выкачать все данные из базы и переместить в основную 
	connection_backup.close()

	#try:
	with open(beckup_db_name, 'r') as becup_file:
		bot.send_document(message.chat.id, becup_file)
	#except:
	#	bot.send_message(message.chat.id, 'Не вышло:(')

	#print(f'{message.chat.id}: Сборка окончена')
	Log_heandler().save_log(f'{message.chat.id}: Сборка окончена')

	os.remove(beckup_db_name)

@bot.message_handler(commands=['get_file'])
def get_file(message):
	if message.chat.id == admin_id:
		text = message.text.split(' ')
		if len(text) < 2:
			bot.send_message(message.chat.id, 'ERRROR: Введите имя файла /get_file file_name.format')
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


on_try = Database_Mgt().project_in_server() # понимаем, где запущен код

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


