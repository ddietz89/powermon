import MySQLdb

class Database(object):
    def __init__(self):
        self.db = None
	self.cursor = None

    def connect(self, host, user, passwd, db):
        if self.db is None:
            self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
	    self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
	    self.db.commit()
	    return True
	except Exception as e:
	    print e
	    return False

    def query(self, sql):
        try:
	    self.cursor.execute(sql)
	    return self.cursor.fetchall()
	except Exception as e:
	    print e
	    return None

    def escape(self, string):
        return MySQLdb.escape_string(string)
