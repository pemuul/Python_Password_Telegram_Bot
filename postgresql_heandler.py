import json
import datetime

#from sqllite_main import Database
from postgresql_main import Database
from loging import Log_heandler

DB_LOCATION = "db_sqlite.sqlite"

class Table(object):
	# схема таблиц хранится в файле shem_table.json
	with open("shem_table.json", "r") as read_file:
		shem_json = json.load(read_file)

	log = Log_heandler()

	def __init__(self, table_name_P, db_name_P=DB_LOCATION, local_db_P=True):
		self.db = Database(db_name_P, local_db_P) # на сервере коннект произойдёт напрямую в базу postgresql, иначе в локалтную sqlite
		self.table_name = table_name_P
		self.shem_table = self.shem_json[table_name_P]['always_fild']
		self.table_key = self.shem_json[table_name_P]['key']

		self.db.create_table(table_name_P, self.shem_json[table_name_P])

	def create_password_table(self):
		self.db.create_table(self.table_name, self.shem_table)

	@log.save_error_log_bool_dec
	def insert(self, *data_P):
		data = data_P
		if "Create date" in self.shem_table:
			now = datetime.datetime.now().strftime("%d_%m_%Y %H:%M:%S")
			data = self.add_by_index([s for s in data_P], now, self.shem_table.index("Create date"))
			print(data)
		self.db.insert_data(self.table_name, self.shem_table, data)
		return True

	def delete(self, *data_P):
		try:
			self.db.delete_data(self.table_name, self.table_key, data_P)
			return True
		except Exception as e:
			Log_heandler().save_log(f'delete table {self.table_name} {data_P} | {e}', 'ERROR')
			return False

	@log.save_error_log_list_dec
	def get(self, *key_P):
		return self.db.get_data(self.table_name, key_P, self.table_key)

	@log.save_error_log_list_dec
	def find_set(self, *key_P):
		return self.db.find_set(self.table_name, key_P, self.table_key)

	@log.save_error_log_list_dec
	def get_log(self, *key_P):
		return self.get(*key_P)

	def get_all(self):
		return self.db.get_table(self.table_name)

	def add_by_index(self, list_P, add_item_P, index_P):
		new = list_P[:index_P]
		new.append(add_item_P)
		return new + list_P[index_P:]

	def select(self, *args, **kwards):
		self.db.select(*args, **kwards)

if __name__ == '__main__':
	Table_password = Table('users_password')

	Table_password.insert(1087624586, 'qwertyd', 'qwrty')
	#print(Table_password.get('123', 'asd'))

	print(Table_password.get(1087624586, 'qwertyd'))

	#print(Table_password.get_all())

	print(Table_password.select('''SELECT * FROM users_password WHERE "User_ID" = '1087624586' and "Description" = 'qwertyd' ''', True))

	#print(Table_password.select('SELECT * FROM "users_password"'))

	#print(Table_password.add_by_index([1, 2, 3, 4, 5, 6, 7, 8], 'd', 4))

	#print(Table_password.shem_by_table_name('users_password'))
	#print(Log_heandler().get_tooday_log())
