import datetime

class Log_heandler:
	def save_log(self, text_P):
		print(text_P)
		with open(f'log/log_{text_P[:10]}.txt', 'a+') as file_log:
			file_log.writelines(text_P + '\n')

	def get_tooday_log(self):
		now_date = datetime.datetime.now().strftime("%d_%m_%Y")
		#print(now_date)
		with open(f'log/log_{now_date}.txt', 'r+') as file_log:
			log_list = file_log.read()

		return log_list
