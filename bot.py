import telebot

import bot_setup
from bot_handler import Handler

bot = telebot.TeleBot(bot_setup.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	handler.send_welcome(message)

@bot.message_handler(content_types=['text'])
def get_text_messages2(message):
	handler.get_text_messages(message)

handler = Handler(bot)
handler.run_bot()
