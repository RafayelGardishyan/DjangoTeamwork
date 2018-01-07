import sqlite3 as s
import logging

class db():	
	logger = logging.getLogger('DBConnection')
	hdlr = logging.FileHandler('dbconnection.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)

	def connect(self, dbname):
		self.db = s.connect(dbname)
		self.logger.info("Connected to database " + dbname)
		
	def disconnect(self, ):
		self.db.close()
		self.logger.info("Disconnected from database")
		
	def cursor(self, ):
		self.cursor = self.db.cursor()
		self.logger.info("Initialized cursor")

	def createtasktable(self, ):
		try:
			query = "CREATE TABLE tasks(id INTEGER PRIMARY KEY, task TEXT, author TEXT)"
			self.cursor.execute(query)
			self.db.commit()
			self.logger.info("Created table tasks")
			return True
		except:
			print("Table already exists")
			self.logger.info("Table tasks already exists")

	def addtask(self, task, author):
		try:
			query = "INSERT INTO tasks(task, author) VALUES(?,?)"
			self.cursor.execute(query, (str(task), str(author)))
			self.db.commit()
			self.logger.info("Added task {} for author {} to database".format(task, author))
			return True
		except Exception as e:
			self.logger.error('Failed to add task to database: '+ str(e))
			print("Error: Can not add task to database")
			return False

	def deletetask(self, task, author):
		try:
			query = "DELETE FROM tasks WHERE task = ? AND author = ?"
			self.cursor.execute(query, (str(task), str(author)))
			self.db.commit()
			self.logger.info("Deleted task {} for author {} from database".format(task, author))
			return True
		except Exception as e:
			self.logger.error('Failed to delte task from database: '+ str(e))
			print("Error: Can not delete task {}".format(task))
			return False

	def gettasks(self, author):
		try:
			query = "SELECT * FROM tasks WHERE author=?"
			self.cursor.execute(query, (str(author),))
			self.logger.info("Got tasks for author {} from database".format(author))
			return self.cursor.fetchall()
		except Exception as e:
			self.logger.error('Failed to get tasks from database: '+ str(e))
			print("Error: Can not get tasks for user {}".format(author))
			return False
