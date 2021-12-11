import sqlite3

class SQL_seandler:
    def __init__(self):
        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()

    def create_table(self, table_name_P, fiald_list_P):
        '''
        (title text, artist text, release_date text,
                   publisher text, media_type text)
        '''
        self.cursor.execute(f'''CREATE TABLE {table_name_P} ({fiald_list_P})''')

    def insert_table(self, table_name_P, data_P):
        self.cursor.execute(f'''INSERT INTO {table_name_P} VALUES({data_P})''')
        self.conn.commit()

    def sql_query(self, selekt_P):
        self.cursor.execute(selekt_P)
        result = self.cursor.fetchall()
        print(result)
        return result

    def test1(self, text_P):
        return text_P

if __name__ == '__main__':
    #print(SQL_seandler.test1('11'))
    sql_seandler = SQL_seandler()
    #sql_seandler.create_table('test', 'id INT PRIMARY KEY, text TEXT')
    #sql_seandler.insert_table('test', "33, 'test12'")
    print(sql_seandler.sql_query("SELECT * FROM test "))

