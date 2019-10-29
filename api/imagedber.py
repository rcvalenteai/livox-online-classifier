import mysql.connector
import operator


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


def not_found(keyword):
    """
    if phrase is not found in the database, tries to similar matches or returns '?' image
    :param keyword: entity to find image for
    :return: returns image-id from database
    :rtype: str
    """
    # TODO: remove plurals
    # TODO: check extended vocabulary
    return '67908e21-1cc5-4aaf-8f8c-a6f33ce8c83b'


def get_image(keyword):
    """
    given a keyword search for similar image in livox database
    :param keyword: entity to find image for
    :return: returns path to image
    :rtype: path (str)
    """
    db = MySQLDB.init_db()
    stmt = "SELECT image_id, confidence FROM Labels WHERE label = %s"
    cur = db.insert(stmt, (keyword,))
    results = dict(cur.fetchall())

    stmt = "SELECT image_id FROM Tags WHERE tag = %s"
    cur = db.insert(stmt, (keyword,))
    results2 = list(cur.fetchall())
    for result in results2:
        if result[0] in results.items():
            results[result[0]] = results[result[0]] + 0.85
        else:
            results[result[0]] = 0.85
    try:
        max_val = max(results.items(), key=operator.itemgetter(1))
    except ValueError:
        max_val = (not_found(keyword),)
    stmt = "SELECT location FROM Images WHERE image_id = %s"
    cur = db.insert(stmt, (max_val[0],))
    results3 = list(cur.fetchall())
    for result in results3:
        path = result
    path = "https://storage.googleapis.com/livox-images/full/" + path[0]
    return path
