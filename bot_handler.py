#pip install PyTelegramBotAPI

import numexpr as ne
import json
import cryptocode
import os

from telebot import types
#from sqllite_heandler import Table
from postgresql_heandler import Table

import bot_setup

#admin_id = bot_setup.ADMIN_ID
admin_id = int(os.environ.get('ADMIN_ID'))

add_password = '''ДОБАВИТЬ НОВЫЙ ПАРОЛЬ:
    Вводишь название (описание) пароля
    Например:
        Яндекс
    Отправляем
    Бот повторит ваше название и предложит варианты
    Надо нажать на кнопку Добавить пароль
    Теперь бот предложит ввести пароль, 
        введите ваш пароль и отправте его
    После отправки бот попросит ввести ключ
        (ключ - это любое слово, цифра, число или буква, 
            что-то что вы не забудите
            Например: 
                последние 4 цифры карты, дата рождения, имя собаки)
        введите ключ и отправте его
    Бот должен ответить Готово, это означает, что ваш ключ сохранён
'''
get_password = '''ПОЛУЧИТЬ ПАРОЛЬ:
    Есть 2 варианта:
        1. Помню точное название пароль
        2. Не помню как называется парль

    1. Помню точное название пароль
        Вводим название пароля, отправляем
        Бот ответит
        Бот повторит ваше название и предложит варианты
        Надо нажать на кнопку Получить пароль
        Теперь надо ввести ключ, который вы вводили при создании
            (ключ - это любое слово, цифра, число или буква,
                что-то что вы не забудите
            Например: 
                    последние 4 цифры карты, дата рождения, имя собаки)
            введите ключ и отправте его
        Бот пришлёт вам пароль
        Если же он ответил False
            Это значит ключ введён неверно

    2. Не помню как называется парль
        Вам надо ввести хотя бы одну букву или 
            часть названия из названия пароля
        Отпавить
        Бот повторит введённое значени и предложит варианты
        Надо нажать на кнопку Показать похожие    
        У вас появиятся все названия поролей схожие 
            с введённым вами значением
            Если похожих много, список можно прокручивать
        Выберите нужный вам и нажмите на него
        Теперь вернитесь к первому варианту 
            (1. Помню точное название пароль)
            и продолжайте с 3 строчки (Бот повторит ваше назв...)
'''
delete_password = '''УДАЛИТЬ ПАРОЛЬ:
    Есть 2 варианта:
        1. Помню точное название пароль
        2. Не помню как называется парль

    1. Помню точное название пароль
        Вводим название пароля, отправляем
        Бот ответит
        Бот повторит ваше название и предложит варианты
        Надо нажать на кнопку Удалить пароль
        Бот ответит Пароль удалён
        Готово

    2. Не помню как называется парль
        Вам надо ввести хотя бы одну букву или часть 
            названия из названия пароля
        Отпавить
        Бот повторит введённое значени и предложит варианты
        Надо нажать на кнопку Показать похожие    
        У вас появиятся клавиатура где все названия поролей 
            схожие с введённым вами значением
            Если похожих много, список можно прокручивать
        Выберите нужный вам и нажмите на него
        Теперь вернитесь к первому варианту 
            (1. Помню точное название пароль)
            и продолжайте с 3 строчки (Бот повторит ваше назв...)
'''

start_text = f'''Я буду хранить твои пароли. 
Даже мой создатель не сможет узнать твой пароль, так как он закдирован, и ключ нигде не хранится.

Как мною пользоваться:

ДОБАВИТЬ НОВЫЙ ПАРОЛЬ:
    /add_password <- тыкай сюда, чтобы узнать

ПОЛУЧИТЬ ПАРОЛЬ:
    /get_password <- тыкай сюда, чтобы узнать

УДАЛИТЬ ПАРОЛЬ:
    /delete_password <- тыкай сюда, чтобы узнать

'''


def my_print(text_P):
	print(text_P)

class Handler:
	def __init__(self, bot):
		self.bot = bot
		self.last_message = None

		self.Table_password = Table('users_password')
		self.Users = Table('users')

		with open("shem_button.json", "r", encoding='utf-8') as read_file:
			self.shem_json = json.load(read_file)

		self.user_insert_password = {}
		self.user_get_password = {}
		self.message_to_delete = {}
		self.global_params = {}

	def send_welcome(self, message):
		# при нажатии на вспомогательную команду возвращаем подсказку 
		my_print(message.json['text'])
		comand = message.json['text']
		if comand in ['/start', '/help']:
			reply_text = start_text
		elif comand == '/add_password':
			reply_text = add_password
		elif comand == '/get_password':
			reply_text = get_password
		elif comand == '/delete_password':
			reply_text = delete_password
		else:
			reply_text = 'такой команды нет :('
		reply_text += '\n /help - тыкай сюда, чтобы получить подсказку'
		self.bot.reply_to(message, reply_text)

	def button_answer(self, call_P):
		# при нажатии на кнопку под сообщением
		params = call_P.data.split(', ')
		return_val = ''
		delete_new_message = False
		message_send = None
		if params[0] == 'Get':
			# при нажатии на кнопку Получить пароль
			get_table = self.Table_password.get(call_P.message.chat.id, params[1])
			if get_table != []:
				self.user_get_password[call_P.message.chat.id] = get_table[2]
				return_val = 'Введите ключ'
				delete_new_message = True
			else:
				return_val = 'Такой записи нет'

		elif params[0] == 'Insert':
			# при нажатии на кнопку Добавить пароль
			if self.Table_password.get(call_P.message.chat.id, params[1]) == []:
				return_val = 'Введите пороль'
				self.user_insert_password[call_P.message.chat.id] = {'description' : params[1], 'password' : '', 'message_id' : call_P.message.message_id}
			else:
				return_val = 'Такое название занято, придумайте другое'

		elif params[0] == 'Delete':
			# если нажата кнопка Удалить пароль
			if self.Table_password.delete(call_P.message.chat.id, params[1]):
				return_val = 'Пороль удалён'
			else:
				return_val = 'Произошла какая-то ошибка'
		elif params[0] == 'Delete_button':
			pass # всё удалится само ниж

		elif params[0] == 'FindSet':
			# выводим клавиатуру похожих записей
			get_table = self.Table_password.find_set(call_P.message.chat.id, params[1])
			if get_table != [[]]:
				print(get_table)
				self.delete_this_message(call_P.message.chat.id,call_P.message.message_id)
				message_send = self.bot.send_message(call_P.message.chat.id, 
						f'Схожие с : {params[1]}', 
						reply_markup=self.create_markup('set_name', [[g[1]] for g in get_table]))
				return_val = f'Схожие с : {params[1]}'
				delete_new_message = True
			else:
				return_val = 'Таких записей нет'
		else:
			pass

		if return_val == '':
			self.delete_this_message(call_P.message.chat.id,call_P.message.message_id)
			return()
		if message_send == None:
			message_send = self.bot.edit_message_text(f"{return_val}", call_P.message.chat.id,call_P.message.message_id)
		#else:
		#	message_send = self.bot.edit_message_text(f"{return_val}", call_P.message.chat.id,call_P.message.message_id,reply_markup=self.create_markup('set_name', return_val))
		#print(message_send.message_id)
		if delete_new_message:
			self.add_message_to_delete(call_P.message.chat.id, message_send.message_id)

	def get_text_messages(self, message):
		self.last_message = message
		self.answer(message)

	def admin(self, text_message_P, message):
		if message.from_user.id == admin_id:	
			if text_message_P == 'admin':
				self.bot.send_message(message.from_user.id, 'Доступ получен', reply_markup=self.create_markup_not_data('admin'))
				return True
			else:	
				return False
		else:
			return False
		

	def answer(self, message):
		# основная функция, обрабатывает пришедьшие пользователем сообщения
		text_message = message.json['text']
		if self.admin(text_message, message):
			return()

		self.new_user(message)

		text_answer = text_message

		self.delete_message_for_user(message.chat.id) 

		if message.chat.id in [i for i in self.user_get_password.keys()]:
			print(self.user_get_password)
			text_answer = cryptocode.decrypt(self.user_get_password[message.chat.id], text_message)
			if text_answer == False:
				text_answer = 'Ключ не подошёл'
			del self.user_get_password[message.chat.id]
			#self.bot.delete_message(message.from_user.id,message.message_id)
			self.delete_this_message(message.from_user.id,message.message_id)
			message_send = self.bot.send_message(message.from_user.id, text_answer, reply_markup=self.create_inline_keyboard('delete_button', text_message))
			self.add_message_to_delete(message.from_user.id, message_send.message_id)

		elif message.chat.id in [i for i in self.user_insert_password.keys()]:
			delete_new_message = False
			if self.user_insert_password[message.chat.id]['password'] == '':
				text_answer = 'Теперь введи ключ'
				#self.bot.delete_message(message.from_user.id,self.user_insert_password[message.chat.id]['message_id'])
				self.delete_this_message(message.from_user.id,self.user_insert_password[message.chat.id]['message_id'])
				#self.user_insert_password[message.chat.id]['message_id'] = message.message_id
				self.user_insert_password[message.chat.id]['password'] = text_message
				delete_new_message = True
			else:
				if self.Table_password.insert(message.chat.id, self.user_insert_password[message.chat.id]['description'], cryptocode.encrypt(self.user_insert_password[message.chat.id]['password'], text_message)):
					text_answer = 'Готово'
				else:
					text_answer = 'Что-то пощло не так, попробуйте ещё раз.'
				#self.bot.delete_message(message.from_user.id,self.user_insert_password[message.chat.id]['message_id'])
				del self.user_insert_password[message.chat.id]
				
			#self.bot.delete_message(message.from_user.id,message.message_id)
			message_send = self.bot.send_message(message.from_user.id, text_answer)
			if delete_new_message:
				self.add_message_to_delete(message.from_user.id, message_send.message_id)
			self.delete_this_message(message.from_user.id,message.message_id)
		else:
			if self.Table_password.get(message.from_user.id, text_message):
				reply_markup = self.create_inline_keyboard('qwery_get', text_message)
			else:
				reply_markup = self.create_inline_keyboard('qwery_find', text_message)
			my_print(f'{self.get_name(message)} : {text_message}')
			my_print(f'|bot|: {text_answer}')
			message_send = self.bot.send_message(message.from_user.id, text_answer, reply_markup=reply_markup)
			self.add_message_to_delete(message.from_user.id, message_send.message_id)

	def delete_this_message(self, user_id_P, message_id_P):
		# удаляем сообщение и удаляем из саиска на очередь удаления, если оно там есть
		message_set = self.message_to_delete.get(user_id_P)
		if message_set != None:
			if message_id_P in message_set:
				del self.message_to_delete[user_id_P][message_set.index(message_id_P)]
		self.bot.delete_message(user_id_P, message_id_P)


	def add_message_to_delete(self, user_id_P, message_id_P):
		# добавляем сообшение в очередь на удаление
		if self.message_to_delete.get(user_id_P) == None:
			self.message_to_delete[user_id_P] = []	
		if not message_id_P in self.message_to_delete[user_id_P]:
			self.message_to_delete[user_id_P].append(message_id_P)

	def delete_message_for_user(self, user_id_P):
		# удаляем все сообщения из очереди на удаление для данного пользователя
		if self.message_to_delete.get(user_id_P) != None:
			for message_id in self.message_to_delete[user_id_P]:
				self.bot.delete_message(user_id_P,message_id)
			del self.message_to_delete[user_id_P]

	def create_markup_not_data(self, shem_button_name_P):
		shem_menu_button = self.shem_json[shem_button_name_P]
		row_list = [str(i) for i in shem_menu_button.keys()]
		markup = types.ReplyKeyboardMarkup(True, True)
		for row_name in row_list:
			row_button = [str(i) for i in shem_menu_button[row_name].keys()]
			btn = [types.KeyboardButton(b) for b in row_button]
			markup.row(*btn)
		return markup

	def create_markup(self, shem_button_name_P, data_to_button_P=[[]]):
		shem_menu_button = self.shem_json[shem_button_name_P]
		row_list = [str(i) for i in shem_menu_button.keys()]
		markup = types.ReplyKeyboardMarkup(True, True)
		row_button = [str(i) for i in shem_menu_button[row_list[0]].keys()]
		for data in data_to_button_P:
			btn = []
			for i in range(len(row_button)):
				b = row_button[i].replace(f'%{i + 1}', data[i])
				btn.append(types.KeyboardButton(b))
				print(b)
			markup.row(*btn)
		return markup

	def create_inline_keyboard(self, shem_button_name_P, text_message_P):
		shem_menu_button = self.shem_json[shem_button_name_P]
		row_list = [str(i) for i in shem_menu_button.keys()]
		markup = types.InlineKeyboardMarkup()
		for row_name in row_list:
			row_button = [str(i) for i in shem_menu_button[row_name].keys()]
			btn = [types.InlineKeyboardButton(b, callback_data=f"{shem_menu_button[row_name][b]['Return_value']}, {text_message_P}") for b in row_button]
			markup.row(*btn)
		return markup

	def get_name(self, message):
		last_name = ''
		first_name = ''
		try:
			last_name = message.from_user.last_name
			if last_name == None:
				last_name = ''
		except:
			pass
		try:
			first_name = message.from_user.first_name
		except:
			pass
		return f'{last_name} {first_name}'

	def run_bot(self):
		self.bot.send_message(admin_id, 'Бот Save_Password_bot был запущен')
		self.bot.polling(none_stop=True) # потом удалить
		last_message = f'Bye! User {self.get_name(self.last_message)} kill me :('
		my_print(last_message)
		self.bot.send_message(admin_id, last_message)

	def new_user(self, message_P):
		if self.Users.get(message_P.chat.id) == []:
			print(self.Users.insert(message_P.chat.id, self.get_name, None, 'Nother'))
			self.bot.send_message(admin_id, f'{str(self.get_name(message_P))} - теперь с нами')

if __name__ == '__main__':
	h = Handler(bot = '')
	#h.add_message_to_delete(12445, 234243)
	h.create_markup('set_name', [['1'],['2'],['3'],['4'],['5']])
	#[print(i.split('-')[1]) for i in str_rule.split('\n')]