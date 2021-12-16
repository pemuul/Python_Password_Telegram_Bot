#pip install PyTelegramBotAPI

import numexpr as ne
import json
import cryptocode

from telebot import types
from sql_seandler import SQL_seandler
from sqllite_heandler import Table


import bot_setup

admin_id = bot_setup.ADMIN_ID

def my_print(text_P):
	print(text_P)

class Handler:
	def __init__(self, bot):
		self.bot = bot
		self.last_message = None
		#self.convert = Convert_base()
		self.sql_seandler = SQL_seandler()

		self.Table_password = Table('users_password')
		self.Users = Table('users')

		with open("shem_button.json", "r", encoding='utf-8') as read_file:
			self.shem_json = json.load(read_file)

		self.user_insert_password = {}
		self.user_get_password = {}

	def send_welcome(self, message):
		my_print(message.json['text'])
		self.bot.reply_to(message, f'Я буду хранить твои пороли. Даже мой создатель не сможет узнать твой пороль, так как он закдирован, и ключ нигде не хранится.')

	def button_answer(self, call_P):
		params = call_P.data.split(',')
		return_val = 'pass'
		if params[0] == 'Get':
			get_table = self.Table_password.get(call_P.message.chat.id, params[1])
			if get_table != []:
				self.user_get_password[call_P.message.chat.id] = get_table[2]
				return_val = 'Введите ключ'
			else:
				return_val = 'Такой записи нет'
		elif params[0] == 'Insert':
			if self.Table_password.get(call_P.message.chat.id, params[1]) == []:
				return_val = 'Введите пороль'
				#if not call_P.message.chat.id in [str(i) for i in self.user_insert_password.keys()]:
				self.user_insert_password[call_P.message.chat.id] = {'description' : params[1], 'password' : '', 'message_id' : call_P.message.message_id}
			else:
				return_val = 'Такое название занято, придумайте другое'
		elif params[0] == 'Delete':
			pass
		else:
			pass

		self.bot.edit_message_text(f"{return_val}", call_P.message.chat.id,call_P.message.message_id)

	def get_text_messages(self, message):
		self.last_message = message
		self.answer(message)

	def admin(self, text_message_P, message):
		if message.from_user.id == admin_id:	
			if text_message_P == 'admin':
				self.bot.send_message(message.from_user.id, 'Доступ получен', reply_markup=self.create_markup('admin'))
				return True
			else:	
				return False
		else:
			return False
		

	def answer(self, message):
		text_message = message.json['text']
		if self.admin(text_message, message):
			return()

		''''''''''''''''''''''''''''''''''''''

		if self.Users.get(message.chat.id) == []:
			print(self.Users.insert(message.chat.id, self.get_name, None, 'Nother'))
		text_answer = text_message

		''''''''''''''''''''''''''''''''''''''
		if message.chat.id in [i for i in self.user_get_password.keys()]:
			print(self.user_get_password)
			text_answer = cryptocode.decrypt(self.user_get_password[message.chat.id], text_message)
			del self.user_get_password[message.chat.id]
			self.bot.delete_message(message.from_user.id,message.message_id)
			self.bot.send_message(message.from_user.id, text_answer)
		
		elif message.chat.id in [i for i in self.user_insert_password.keys()]:
			if self.user_insert_password[message.chat.id]['password'] == '':
				text_answer = 'Теперь введи ключ'
				self.bot.delete_message(message.from_user.id,self.user_insert_password[message.chat.id]['message_id'])
				#self.user_insert_password[message.chat.id]['message_id'] = message.message_id
				self.user_insert_password[message.chat.id]['password'] = text_message
			else:
				if self.Table_password.insert(message.chat.id, self.user_insert_password[message.chat.id]['description'], cryptocode.encrypt(self.user_insert_password[message.chat.id]['password'], text_message)):
					text_answer = 'Готово'
				else:
					text_answer = 'Что-то пощло не так, попробуйте ещё раз.'
				#self.bot.delete_message(message.from_user.id,self.user_insert_password[message.chat.id]['message_id'])
				del self.user_insert_password[message.chat.id]
				

			self.bot.delete_message(message.from_user.id,message.message_id)
			self.bot.send_message(message.from_user.id, text_answer)
		else:
			my_print(f'{self.get_name(message)} : {text_message}')
			my_print(f'|bot|: {text_answer}')
			self.bot.send_message(message.from_user.id, text_answer, reply_markup=self.create_inline_keyboard('qwery', text_message))

	def create_markup(self, shem_button_name_P):
		shem_menu_button = self.shem_json[shem_button_name_P]
		row_list = [str(i) for i in shem_menu_button.keys()]
		markup = types.ReplyKeyboardMarkup(True, True)
		for row_name in row_list:
			row_button = [str(i) for i in shem_menu_button[row_name].keys()]
			btn = [types.KeyboardButton(b) for b in row_button]
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
		except:
			pass
		try:
			first_name = message.from_user.first_name
		except:
			pass
		return f'{last_name} {first_name}'

	def run_bot(self):
		self.bot.send_message(admin_id, 'Бот Pem_Test_bot был запущен')
		self.bot.polling(none_stop=True) # потом удалить
		last_message = f'Bye! User {self.get_name(self.last_message)} kill me :('
		my_print(last_message)
		self.bot.send_message(admin_id, last_message)

if __name__ == '__main__':
	pass