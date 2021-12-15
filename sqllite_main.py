import sqlite3

class Database:
	"""sqlite3 database class that holds testers jobs"""
	DB_LOCATION = "tester_db.sqlite"

	def __init__(self, database_name_P):
		"""Initialize db class variables"""
		self.connection = sqlite3.connect(database_name_P, check_same_thread=False)
		#self.table_name = table_name_P
		self.cur = self.connection.cursor()

	def close(self):
		"""close sqlite3 connection"""
		self.connection.close()

	def execute(self, new_data):
		"""execute a row of data to current cursor"""
		self.cur.execute(new_data)

	def executemany(self, many_new_data):
		"""add many new data to database in one go"""
		self.create_table()
		self.cur.executemany('REPLACE INTO jobs VALUES(?, ?, ?, ?)', many_new_data)

	def create_table(self, table_name_P, row_list_P, key_list_P, hard_create_P=False):
		"""create a database table if it does not exist already"""
		self.cur.execute(f'''SELECT name FROM sqlite_master 
								WHERE name='{table_name_P}' ''')
		
		#if self.cur.fetchall() != [] and not hard_create_P:
		#	return()

		row_line = '", "'.join(row_list_P)
		row_line = f'"{row_line}"'
		key_list = '", "'.join(key_list_P)
		key_list = f'"{key_list}"'
		self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_P}({row_line}, primary key ({key_list}))''')

	def commit(self):
		"""commit changes to database"""
		self.connection.commit()

	def get_table(self, table_name_P):
		self.cur.execute(f'SELECT * FROM {table_name_P}')
		return self.cur.fetchall()

	def insert_data(self, table_name_P, line_name_P, data_line_P):
		line_name = '", "'.join([str(i) for i in line_name_P])
		line_name = f'"{line_name}"'
		data_line = "', '".join([str(i) for i in data_line_P])

		#print(f"INSERT INTO {table_name_P} ({line_name}) VALUES('{data_line}')")
		print(f"INSERT INTO {table_name_P} ({line_name}) VALUES('{data_line}')")
		self.cur.execute(f"INSERT INTO {table_name_P} ({line_name}) VALUES('{data_line}')")
		self.commit()

	def get_data(self, table_name_P, key_data_P, key_P):
		key_data = ", ".join([str(i) for i in key_data_P])
		key = ", ".join([str(i) for i in key_P])
		filter_set = ''#[[f'{str(key_data_P[i])}, {str(key_P[i])}'] for i in range(len(key_P))]
		for i in range(len(key_P)):
			filter_set += f"{str(key_P[i])} = '{str(key_data_P[i])}' and "
		filter_set = filter_set[:-4]

		print(f'SELECT * FROM {table_name_P} WHERE {filter_set}')
		self.cur.execute(f'SELECT * FROM {table_name_P} WHERE {filter_set}')
		return self.fetchall_to_list(self.cur.fetchall())

	def select(self, text_P):
		self.cur.execute(text_P)
		return self.cur.fetchall()

	def fetchall_to_list(self, fetchall_P):
		if len(fetchall_P) > 0:
			return [fetch for fetch in fetchall_P[0]]
		else:
			return []

	def add_colum(self, table_name_P, field_name_P, field_type_P):
		return self.select(f'alter table {table_name_P} add "{field_name_P}" {field_type_P}')

if __name__ == '__main__':
	db = Database('tester_db.sqlite')
	#db.create_table('users_password', ["User_ID integer", 
	#					"Description text",
	#					"Password text", 'primary key  (User_ID, Description)'])
	
	#db.insert_data('users_password', ["User_ID", "Description", "Password"], ['13', '14124', '1234'])
	#db.commit()
	#print(db.get_data('users_password'))
	#db.get_data('users_password', ['1', '2', '3'], ['4', '5', '6'])
	#print(db.select('alter table users_password add "Create date"'))
	#print([i for i, b in map(32, [134,34,3])])
	#for i, b in map(1, ['134','34','3']):
	#	print(i, b)
	#print([i + b for i, b in (['1', '2', '3'], ['4', '5', '6'])])
