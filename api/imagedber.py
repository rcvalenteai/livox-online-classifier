import mysql.connector
import operator
from nltk.stem import PorterStemmer
import json
import datetime



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


# db = MySQLDB.init_db()

def not_found(keyword, db=None):
    """
    if phrase is not found in the database, tries to similar matches or returns '?' image
    :param keyword: entity to find image for
    :return: returns image path from database
    :rtype: str
    """
    path = 'symbol00071621.png'
    try:
        path = search_image_word(keyword[:-1], db)
    except ValueError:
        try:
            path = stemmed(keyword, db)
        except ValueError:
            try:
                path = translate(keyword, db)
            except ValueError or KeyError:
                try:
                    path = closest(keyword, db)
                except ValueError:
                    pass
    return path
    # TODO: remove plurals
    # TODO: check extended vocabulary


def stemmed(keyword, db=None):
    """
    stem the phrase and search
    :param keyword: entity to find image for
    :return: image path from database
    :rtype: str
    """
    ps = PorterStemmer()
    words = keyword.split()
    for word in words:
        word = ps.stem(word)
    words = " ".join(words)
    return search_image_word(keyword, db)


def closest(keyword, db=None):
    """
    look through the closest words for an image
    :param keyword: entity to find image for
    :param db: db to look through
    :return: image path from database
    :rtype: str
    """
    with open('./resources/extened-vocab-cleaned.json', 'r', encoding='utf-8') as f:
        vocab = json.loads(f.read())
    path = None
    if keyword in vocab:
        words = vocab[keyword]
        for word in words:
            if path is None:
                try:
                    path = search_image_word(word, db)
                except ValueError:
                    pass
            else:
                break
    if path is None:
        raise ValueError
    return path


def translate(keyword, db=None):
    """
    use known vocab translation to get word in database
    :param keyword: entity to find image for
    :param db: db to look through
    :return: image path from database
    :rtype: str
    """
    path = None
    with open('./resources/extened-vocab-translate.json', 'r', encoding='utf-8') as f:
        vocab = json.loads(f.read())
    try:
        if keyword in vocab:
            path = search_image_word(vocab[keyword], db=None)
    except ValueError:
        raise
    if path is None:
        raise ValueError
    return path


def search_tags(keyword, db=None):
    """
    search livox tags
    :param keyword:
    :param db:
    :return: list of image_ids found
    """
    image_ids = dict()
    words = keyword.split()
    for word in words:
        stmt = "SELECT image_id FROM Tags WHERE tag = %s"
        cur = db.insert(stmt, (keyword,))
        results2 = list(cur.fetchall())
        for result in results2:
            if result in image_ids:
                image_ids[result].append(word)
            else:
                image_ids[result] = list()
                image_ids[result].append(word)
    image_ids_ls = list()
    # only complete matches
    for key, value in image_ids.items():
        if len(value) == len(words):
            image_ids_ls.append(key)
    # least tagged closest match first
    final_images = list()
    # print(image_ids_ls)
    for id in image_ids_ls:
        stmt = "SELECT tag FROM Tags WHERE image_id = %s"
        cur = db.insert(stmt, (id[0], ))
        results = list(cur.fetchall())
        size = len(results)
        final_images.append((id[0], size))
    return final_images


def search_image_word(keyword, db=None):
    """
    searches database for keyword
    :param keyword: entity to find image for
    :param db: db to look through
    :return: image relative path
    :rtype: str
    """
    if db is None:
        db = MySQLDB.init_db()
    stmt = "SELECT image_id, confidence FROM Labels WHERE label = %s"
    cur = db.insert(stmt, (keyword,))
    results = dict(cur.fetchall())

    # stmt = "SELECT image_id FROM Tags WHERE tag = %s"
    # cur = db.insert(stmt, (keyword,))
    # results2 = list(cur.fetchall())
    results2 = search_tags(keyword, db)
    for result in results2:
        if result[0] in results.items():
            results[result[0]] = results[result[0]] + 0.85 # - (result[1] * .005)
        else:
            results[result[0]] = 0.85 # - (result[1] * .005)
        #print(results[result[0]])
    try:
        max_val = max(results.items(), key=operator.itemgetter(1))
    except ValueError:
        raise
    stmt = "SELECT location FROM Images WHERE image_id = %s"
    cur = db.insert(stmt, (max_val[0],))
    results3 = list(cur.fetchall())
    path = ''
    for result in results3:
        path = result
    return path[0]


def get_image(keyword, db=None):
    """
    given a keyword search for similar image in livox database
    :param keyword: entity to find image for
    :return: returns path to image
    :rtype: path (str)
    """
    if db is None:
        db = MySQLDB.init_db()
    try:
        path = search_image_word(keyword, db)
    except ValueError:
        path = not_found(keyword, db)
    path = "https://storage.googleapis.com/livox-images/full/" + path
    return path


def get_image_test(keyword, db=None):
    """
    given a keyword search for similar image in livox database
    :param keyword: entity to find image for
    :return: returns path to image
    :rtype: path (str)
    """
    if db is None:
        db = MySQLDB.init_db()
    try:
        path = search_image_word(keyword, db)
    except ValueError:
        path = not_found(keyword, db)
    path = "https://storage.googleapis.com/livox-images/full/" + path
    return (path, db)
