import telebot
import datetime

import bot_setup
from bot_handler import Handler
from loging import Log_heandler

bot = telebot.TeleBot(bot_setup.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	handler.send_welcome(message)

@bot.message_handler(content_types=['text'])
def get_text_messages2(message):
	handler.get_text_messages(message)

while True:
	try:
		handler = Handler(bot)
		handler.run_bot()
	except Exception as e:
		try:
			now = datetime.datetime.now().strftime("%d_%m_%Y %H:%M:%S")
			Log_heandler().save_log(f'{now} | {e}')
			#print(f'{now} | {e}')
		except:
			print('ERROR try log')
