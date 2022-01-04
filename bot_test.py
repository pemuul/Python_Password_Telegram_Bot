import telebot
import datetime
import os

import bot_setup
from bot_handler import Handler
from loging import Log_heandler
from sqllite_main import Database
from telebot import types

bot = telebot.TeleBot(bot_setup.TOKEN)
to_delete = {}
count = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Доров')

@bot.message_handler(commands=['add_colum'])
def get_log(message):
	bot.send_message(message.chat.id, 'Ok', reply_markup=test())

@bot.message_handler(content_types=['text'])
def get_text_messages2(message):
	global count
	message_send = bot.send_message(message.chat.id, 'Пук', reply_markup=test())
	bot.delete_message(message.chat.id,message.message_id)
	delete_message_for_user(message.chat.id)
	add_message_to_delete(message.chat.id,message_send.message_id)
	if int(get_count(message.chat.id)%10) == 0:
		bot.send_message(message.chat.id, f'Уже {get_count(message.chat.id)} очков!', reply_markup=test())
	get_count(message.chat.id, 1)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	handler.button_answer(call)

def add_message_to_delete(user_id_P, message_id_P):
	if to_delete.get(user_id_P) == None:
		to_delete[user_id_P] = {}
	to_delete[user_id_P][message_id_P] =  message_id_P
	print(to_delete[user_id_P])

def get_count(user_id_P, plus_P=0):
	if count.get(user_id_P) == None:
		count[user_id_P] = 0
	return_value = count[user_id_P]
	count[user_id_P] += plus_P
	return return_value

def delete_message_for_user(user_id_P):
	if to_delete.get(user_id_P) != None:
		print(to_delete[user_id_P])
		for message_id in [i for i in to_delete[user_id_P].keys()]:
			try:
				bot.delete_message(user_id_P,message_id)
				del to_delete[user_id_P][message_id]
			except:
				print(message_id, '|||||||||||||||||||||||||')

def test():
	markup = types.ReplyKeyboardMarkup(True, False)
	markup.row(types.KeyboardButton('Клик'))
	return markup
	 
while True:
	try:
		print('start')
		bot.polling(none_stop=True) # потом удалить
	except:
		print('Bot restart')