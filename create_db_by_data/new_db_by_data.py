import json
import os
from postgresql_heandler import Table

json_file_name = 'result.json'
beckup_db_name = 'becup.sqlite'

with open(json_file_name, 'r') as becup_file:
	dict_becup = json.load(becup_file)

with open("shem_table.json", "r", encoding='utf-8') as read_file:
	shem_json = json.load(read_file)

try:
	os.remove(beckup_db_name)
	print(f'файл удалён {beckup_db_name}')
except:
	print(f'файл не найден {beckup_db_name}')

for table_name in shem_json:
	table = Table(table_name, beckup_db_name, False)
	db_becup = table.db
	for data in dict_becup[table_name]:
		data = [str(d) for d in data]
		data_set = "', '".join(data)
		line_name = '", "'.join(shem_json[table_name]['always_fild'])
		line_name = f'"{line_name}"'
		execute = f"INSERT INTO {table_name} ({line_name}) VALUES('{data_set}')"
		print(execute)
		db_becup.execute(execute)
		db_becup.commit()
	db_becup.close()








