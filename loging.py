import datetime

class Log_heandler:
	def get_log_name_file(self, now_P = ''):
		if now_P == '':
			now = datetime.datetime.now().strftime("%d_%m_%Y %H:%M:%S")
		else:
			now = now_P
		return f'log/log_{now[:10]}.txt'

	def save_log(self, text_P, type_P=''):
		try:
			now = datetime.datetime.now().strftime("%d_%m_%Y %H:%M:%S")
			str_log = f'{now} | {text_P}'
			if type_P != '':
				str_log = f'{type_P} | {str_log}'
			print(str_log)
			with open(self.get_log_name_file(now), 'a+') as file_log:
				file_log.writelines(str_log + '\n')
			return True
		except:
			print('ERROR try log!')
			return False

	def get_tooday_log(self):
		now_date = datetime.datetime.now().strftime("%d_%m_%Y")
		#print(now_date)
		with open(f'log/log_{now_date}.txt', 'r+') as file_log:
			log_list = file_log.read()[:1000]

		return log_list

	def try_funk(self, func_P, args, kwargs):
		try:
			return func_P(*args, **kwargs)	
		except Exception as e:
			Log_heandler().save_log(f'{e} |args>| {str(args)} |kwargs>| {str(kwargs)}')
			return None

	def save_error_log_list_dec(self, func_P):
		def wraper(*args, **kwargs):
			return_f = self.try_funk(func_P, args, kwargs)
			if return_f != None:
				return return_f
			else:
				return []
		return wraper

	def save_error_log_bool_dec(self, func_P):
		def wraper(*args, **kwargs):
			return_f = self.try_funk(func_P, args, kwargs)
			if return_f != None:
				return return_f
			else:
				return False
		return wraper



if __name__ == '__main__':
	pass