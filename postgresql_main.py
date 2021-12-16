import sqlite3
import psycopg2
import os

class Database:
	"""sqlite3 database class that holds testers jobs"""
	def __init__(self, database_name_P):
		"""Initialize db class variables"""
		if os.getcwd() == '/app':
			self.connection = self.dbConn()
		else:
			self.connection = sqlite3.connect(database_name_P, check_same_thread=False)
		
		#self.table_name = table_name_P
		self.cur = self.connection.cursor()

	def dbConn(self):
		conn = psycopg2.connect(dbname='dac7beqlceqgjn', user='kvwornaibpygwp',
								password='82571b29e5d80ae6c567e343386315e13f84c921544fac2e3a9b10224f24496c',
								host='ec2-35-169-37-64.compute-1.amazonaws.com')
		return conn

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

	def create_table(self, table_name_P, shem_table_name_P, hard_create_P=False):
		shem = shem_table_name_P['shem']
		row_list = [i for i in shem.keys()]


		#row_line = '", "'.join(row_list_P)
		row_line = ''.join([f'"{row}" {shem[row]}, ' for row in row_list])[:-2]
		#print(row_line)
		#row_line = f'"{row_line}"'
		#key_list = '", "'.join(key_list_P)
		#key_list = f'"{key_list}"'
		key_list = ''.join([f'"{i}", ' for i in shem_table_name_P['key']])[:-2]
		#print('CREATE TABLE IF NOT EXISTS users_password("User_ID" INTEGER, "Description" TEXT, "Password" TEXT, "Create date" TEXT, PRIMARY KEY ("User_ID", "Description"))')
		#print(f"CREATE TABLE IF NOT EXISTS {table_name_P}({row_line}, primary key ({key_list}))")
		self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name_P}({row_line}, primary key ({key_list}))")
		
		'''
		CREATE TABLE accounts (
			user_id serial PRIMARY KEY,
			username VARCHAR ( 50 ) UNIQUE NOT NULL,
			password VARCHAR ( 50 ) NOT NULL,
			email VARCHAR ( 255 ) UNIQUE NOT NULL,
			created_on TIMESTAMP NOT NULL,
				last_login TIMESTAMP
		);
		'''
		'''
		self.cur.execute(f"SELECT name FROM sqlite_master 
								WHERE name='{table_name_P}'")
		row_line = '", "'.join(row_list_P)
		row_line = f'"{row_line}"'
		key_list = '", "'.join(key_list_P)
		key_list = f'"{key_list}"'
		self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name_P}({row_line}, primary key ({key_list}))")
		'''

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
			filter_set += f'''"{str(key_P[i])}" = '{str(key_data_P[i])}' and '''
		filter_set = filter_set[:-4]

		print(f'SELECT * FROM {table_name_P} WHERE {filter_set}')
		self.cur.execute(f'SELECT * FROM {table_name_P} WHERE {filter_set}')
		return self.fetchall_to_list(self.cur.fetchall())

	def select(self, text_P, returned_P=True):
		self.cur.execute(text_P)
		self.commit()
		if returned_P:
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
	db.dbConn()
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
