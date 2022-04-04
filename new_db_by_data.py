import json
import os
from postgresql_heandler import Table

json_file_name = 'result.json'
beckup_db_name = 'becup.sqlite'

with open(json_file_name, 'r') as becup_file:
	#print(becup_file)
	dict_becup = json.load(becup_file)
	#print(dict_becup)

with open("shem_table.json", "r", encoding='utf-8') as read_file:
	shem_json = json.load(read_file)
	#print(shem_json.keys())

try:
	os.remove(beckup_db_name)
	print(f'файл удалён {beckup_db_name}')
except:
	print(f'файл не найден {beckup_db_name}')

for table_name in shem_json:
	table = Table(table_name, beckup_db_name, False)
	db_becup = table.db
	#cursor_becup = db_becup.cur
	#print([i[0] for i in table.get_all()])
	#all_data[table_name] = table.get_all()
	#print(table.get_all())
	for data in dict_becup[table_name]:
		#
		data = [str(d) for d in data]
		data_set = "', '".join(data)
		#print(shem_json[table_name]['always_fild'])
		line_name = '", "'.join(shem_json[table_name]['always_fild'])
		line_name = f'"{line_name}"'
		#print(line_name)
		#print(txt)
		#INSERT INTO users_password ("User_ID", "Description", "Password", "Create date") VALUES('1087624586', ' 123', 'W/ak*t+OASENVAHrq7E98UnGLBA==*UO0gAsiCOKNQnIgupNaFOA==*apgKFzivffACl41IEu2qXg==', '16_12_2021 16:58:39'
		execute = f"INSERT INTO {table_name} ({line_name}) VALUES('{data_set}')"
		print(execute)
		#with open('result.json', 'w') as fp:
		#	json.dump(sample, fp)
		db_becup.execute(execute)
		db_becup.commit()
	db_becup.close()








