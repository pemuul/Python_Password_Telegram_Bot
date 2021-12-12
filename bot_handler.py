#pip install PyTelegramBotAPI

#import decimal
import numexpr as ne
from telebot import types
from sql_seandler import SQL_seandler
#from convert import Convert_base
#import sys

import bot_setup

admin_id = bot_setup.ADMIN_ID

def my_print(text_P):
	print(text_P)

class Handler:
	def __init__(self, bot):
		self.bot = bot
		#self.convert = Convert_base()
		self.sql_seandler = SQL_seandler()

	def send_welcome(self, message):
		my_print(message.json['text'])
		#elf.bot.reply_to(message, f'Я бот, который переоводит одно числов другую систему счисления. \n Пример: 5 from 8 to  4\n Это из 5 в восьмеричной системы в четверичную. {message.from_user.first_name}')

	def get_text_messages(self, message):
		self.last_message = message
		self.answer(message)

	def answer(self, message):
		# выключатель для админа
		if message.text.lower() == '0':
			if message.from_user.id == admin_id:
				#pass
				self.bot.stop_polling()
			else:
				self.bot.send_message(message.from_user.id, 'Ну ты пытался', reply_markup=self.create_markup(2, ['5from 6 to 8', '-A1from16', '3123 from 4 to8', '0']))
		text_message = message.json['text']
		my_print(f'{self.get_name(message)} : {text_message}')
			
		#text_answer = self.convert.convert_from_text(text_message)
		text_answer = 'pass'

		my_print(f'|bot|: {text_answer}')
		self.bot.send_message(message.from_user.id, text_answer, reply_markup=self.create_markup(2, ['SELECT * FROM test', '0']))

	def create_markup(self, row_width, items = []):
		markup = types.ReplyKeyboardMarkup(row_width=2)
		btn = []
		for item in items:
			btn = types.KeyboardButton(item)
			btn2 = types.KeyboardButton(item)
			markup.add(btn, btn2)
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