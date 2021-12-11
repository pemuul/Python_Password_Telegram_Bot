import unittest
#from bot_handler import convert_base, Handler
#from convert import Convert_base
from sql_seandler import SQL_seandler

class TestStringMethods(unittest.TestCase):
	def init(self):
		#self.head = Handler(None)
		self.sql_seandler = SQL_seandler()
		self.list_to_test = {
			'  3 from 10 to 2' : '11',
			'3from 10 to 2' : '11',
			'121 from 3to 8' : '20',
			'3123 from 4 to8' : '333',
			'3123 from 4 to 5' : '1334',
			'A2 from 16 to 2' : '10100010',
		}


	def test_convert_all(self):
		self.init()			
		self.assertEqual('11', self.sql_seandler.test1('11'))
		#self.assertEqual('11', convert_base(3, 10, 2))
		'''for item in self.list_to_test:
			#print(f'___{self.list_to_test[item]} | {self.head.make(item)}')
			#self.assertEqual(self.list_to_test[item], self.head.make(item))
			self.assertEqual(self.list_to_test[item], self.convet_f.convert_from_text(item))
		'''

if __name__ == '__main__':
	unittest.main()