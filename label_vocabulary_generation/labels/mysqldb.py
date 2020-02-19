import mysql.connector


# class to handle MySQL interactions
class MySQLDB(object):
    def __init__(self, user, password, host, database):
        self.conn = mysql.connector.connect(user=user, password=password, host=host,
                                            database=database)
        self.cur = self.conn.cursor()
        self.conn.commit()

    """
    returns a initialized database connection with the default parameters
    """
    @classmethod
    def init_db(cls):
        db = MySQLDB(user='livoxmqp', password='livoxmqp2019',
                     host='livoxmqp.ckeabih2gyd2.us-east-1.rds.amazonaws.com', database='livoxmqp')
        return db

    def insert(self, query, params):
        try:
            self.cur.execute(query, params)
        except mysql.connector.IntegrityError as e:
            print(e)
        return self.cur

    def insertmany(self, query, params):
        try:
            self.cur.executemany(query, params)
        except mysql.connector.IntegrityError as e:
            print(e)
        return self.cur

    def query(self, query):
        self.cur.execute(query)
        return self.cur

    def run_script(self, script):
        self.cur.executescript(script)
        return self.cur

    def __del__(self):
        self.conn.commit()
        self.conn.close()