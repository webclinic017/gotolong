import os
import sqlite3

from project import *

class Database(Project):
	def __init__(self):
		super(Database, self).__init__()
		self.debug_level = 0 
		self.db_filename =  'equity.db'
		self.db_filepath = os.path.join(self.project_db_files_get(), self.db_filename)
		db_exists = os.path.exists(self.db_filepath)
		if db_exists:
			print 'db exists'
		else:
			print 'db new'
		self.db_conn = sqlite3.connect(self.db_filepath)
		
		# sqlite3.ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str). It is highly recommended that you instead just switch your application to Unicode strings.
		
		self.db_conn.text_factory = str

	def set_debug_level(self, debug_level):
 		self.debug_level = debug_level

	def db_get_conn(self):
		return self.db_conn
