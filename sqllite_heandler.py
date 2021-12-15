import json

from sqllite_main import Database
from loging import Log_heandler

class Table(object):
	# схема таблиц хранится в файле shem_table.json
	with open("shem_table.json", "r") as read_file:
		shem_json = json.load(read_file)

	log = Log_heandler()

	def __init__(self, table_name_P):
		DB_LOCATION = "tester_db.sqlite"
		self.db = Database(DB_LOCATION)
		self.table_name = table_name_P
		self.shem_table = self.shem_by_table_name(table_name_P)
		#print(self.shem_table)
		self.table_key = self.shem_json[table_name_P]['key']
		#print(self.table_key)

		self.db.create_table(table_name_P, self.shem_table, self.table_key)
		#print(self.table_key)

	def create_password_table(self):
		self.db.create_table(self.table_name, self.shem_table)

	def shem_by_table_name(self, table_name_P):
		try:	
			return [key for key in self.shem_json[table_name_P]['shem'].keys()]
		except:
			return []

	@log.save_error_log_bool_dec
	def insert(self, *data_P):
		try:
			self.db.insert_data(self.table_name, self.shem_table, data_P)
			return True
		except Exception as e:
			Log_heandler().save_log(f'insert table {self.table_name} {data_P} | {e}', 'ERROR')
			return False

	@log.save_error_log_list_dec
	def get(self, *key_P):
		#try:
		return self.db.get_data(self.table_name, key_P, self.table_key)
		#except Exception as e:
		#	Log_heandler().save_log(f'get table {self.table_name} {key_P} | {e}', 'ERROR')
		#	return None

	@log.save_error_log_list_dec
	def get_log(self, *key_P):
		return self.get(*key_P)

	def get_all(self):
		return self.db.get_table(self.table_name)

if __name__ == '__main__':
	Table_password = Table('users_password')

	#Table_password.insert(1087624586, 'qwerty', 'qwrty')
	#print(Table_password.get('123', 'asd'))

	print(Table_password.get(1087624586, 'qwerty'))

	print(Table_password.get_all())

	#print(Table_password.shem_by_table_name('users_password'))
	#print(Log_heandler().get_tooday_log())
