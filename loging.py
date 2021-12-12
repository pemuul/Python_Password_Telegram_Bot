

class Log_heandler:
	def save_log(self, text_P):
		print(text_P)
		with open(f'log/log_{text_P[:10]}.txt', 'a+') as file_log:
			file_log.writelines(text_P + '\n')