import sqlite3
import psycopg2
import os

class Database_Mgt:
	def get_local_database_url(self, database_url_name_P):
		# у нас есть локальная переменная хранящая подключение к postgres, и мы её разбираем, чтобы получить данные для коннекта 
		url_db = os.environ.get(database_url_name_P)
		url_db = url_db[11:]
		len_p = url_db.find(':')
		user_db = url_db[:len_p]
		url_db = url_db[len_p + 1:]

		len_p = url_db.find('@')
		password_db = url_db[:len_p]
		url_db = url_db[len_p + 1:]

		len_p = url_db.find(':')
		host_db = url_db[:len_p]
		url_db = url_db[len_p + 1:]

		len_p = url_db.find('/')
		dbname_db = url_db[len_p + 1:]
		url_db = url_db[len_p + 1:]

		return [dbname_db, user_db, password_db, host_db]

	def project_in_server(self):
		# понимаем, на сервере или локально запущен бот
		#return True
		return os.getcwd() == '/app'

class Database:
	def __init__(self, database_name_P='', local_db_P=True):
		if Database_Mgt().project_in_server() and local_db_P:
			self.connection = self.dbConn() # подключение к базе на сервере 
		else:
			self.connection = sqlite3.connect(database_name_P, check_same_thread=False) # подключение к локально базе данных
		
		self.cur = self.connection.cursor()

	def dbConn(self):
		# распарсиваем локальную переменную DATABASE_URL и формируем подключение к серверу
		database_data = Database_Mgt().get_local_database_url('DATABASE_URL')
		conn = psycopg2.connect(dbname=database_data[0], user=database_data[1],
								password=database_data[2],
								host=database_data[3])
		return conn

	def close(self):
		self.connection.close()

	def execute(self, new_data):
		self.cur.execute(new_data)

	def executemany(self, many_new_data):
		self.create_table()
		self.cur.executemany('REPLACE INTO jobs VALUES(?, ?, ?, ?)', many_new_data)

	def delete_data(self, table_name_P, shem_table_name_P, data_P):
		key_list = shem_table_name_P
		#print('ok2')
		data_P = [str(i) for i in data_P]
		#print(data_P)
		filter_set = ''
		for i in range(len(key_list)):
			filter_set += f'''"{str(key_list[i])}" = '{str(data_P[i])}' and '''
		#print(filter_set)
		filter_set = filter_set[:-4]
		print(f'DELETE FROM {table_name_P} WHERE {filter_set}')
		self.cur.execute(f'DELETE FROM {table_name_P} WHERE {filter_set}')
		self.commit()


	def create_table(self, table_name_P, shem_table_name_P):
		shem = shem_table_name_P['shem']
		row_list = [i for i in shem.keys()]
		row_line = ''.join([f'"{row}" {shem[row]}, ' for row in row_list])[:-2]
		key_list = ''.join([f'"{i}", ' for i in shem_table_name_P['key']])[:-2]
		self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name_P}({row_line}, primary key ({key_list}))")
		self.commit()

	def commit(self):
		self.connection.commit()

	def get_table(self, table_name_P):
		self.cur.execute(f'SELECT * FROM {table_name_P}')
		return self.cur.fetchall()

	def insert_data(self, table_name_P, line_name_P, data_line_P):
		line_name = '", "'.join([str(i) for i in line_name_P])
		line_name = f'"{line_name}"'
		data_line = "', '".join([str(i) for i in data_line_P])

		#print(f"INSERT INTO {table_name_P} ({line_name}) VALUES('{data_line}')")
		ins_execute = f"INSERT INTO {table_name_P} ({line_name}) VALUES('{data_line}')"
		print(ins_execute)
		self.cur.execute(ins_execute)
		self.commit()

	def get_data(self, table_name_P, key_data_P, key_P):
		filter_set = self.select_data_to_key(key_data_P, key_P)

		print(f'SELECT * FROM {table_name_P} WHERE {filter_set}')
		self.cur.execute(f'SELECT * FROM {table_name_P} WHERE {filter_set}')
		return self.fetchall_to_list(self.cur.fetchall())[0]

	def find_set(self, table_name_P, key_data_P, key_P):
		filter_set = self.select_data_to_key(key_data_P, key_P, 'LIKE', '%', '%')

		text = f'''SELECT * FROM {table_name_P} WHERE {filter_set}'''
		print(text)
		self.cur.execute(text)
		return self.fetchall_to_list(self.cur.fetchall())

	def select(self, text_P, returned_P=True):
		self.cur.execute(text_P)
		self.commit()
		if returned_P:
			return self.cur.fetchall()

	def select_data_to_key(self, key_data_P, key_P, primery_P='=', previus_P='',end_P=''):
		filter_set = ''
		for i in range(len(key_P)):
			filter_set += f'''LOWER(CAST("{str(key_P[i])}" AS TEXT)) {primery_P} LOWER('{previus_P}{str(key_data_P[i])}{end_P}') and '''
		filter_set = filter_set[:-4]
		return filter_set


	def fetchall_to_list(self, fetchall_P):
		if len(fetchall_P) > 0:
			return [[f for f in fetch] for fetch in fetchall_P]
			#return [fetch for fetch in fetchall_P[0]]
		else:
			return [[]]

	def add_colum(self, table_name_P, field_name_P, field_type_P):
		return self.select(f'alter table {table_name_P} add "{field_name_P}" {field_type_P}')

if __name__ == '__main__':
	db = Database('db_sqlite.sqlite')
	#db.dbConn()
	#db.create_table('users_password', ["User_ID integer", 
	#					"Description text",
	#					"Password text", 'primary key  (User_ID, Description)'])
	print(db.select('SELECT * FROM users_password'))

	#db.insert_data('users_password', ["User_ID", "Description", "Password"], ['13', '14124', '1234'])
	#db.commit()
	#print(db.get_data('users_password'))
	#db.get_data('users_password', ['1', '2', '3'], ['4', '5', '6'])
	#print([i for i, b in map(32, [134,34,3])])
	#for i, b in map(1, ['134','34','3']):
	#	print(i, b)
	#print([i + b for i, b in (['1', '2', '3'], ['4', '5', '6'])])
