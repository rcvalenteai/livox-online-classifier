import uuid
import datetime
from label_vocabulary_generation.labels.mysqldb import MySQLDB


# this class will take care of logging
class Logs(object):
    """
    logging phrase parsing activity responses from API
    """

    def __init__(self, phrase, is_list=None, question_phrase=None, list_phrase=None, entities=None):
        """
        interface for Logs database table
        :param phrase: full original phrase
        :param is_list: if question was classified as a list classifier
        :param question_phrase:
        :param list_phrase:
        :param entities:
        """
        self.log_id = str(uuid.uuid4())
        self.phrase = phrase
        self.is_list = is_list
        self.question_phrase = question_phrase
        self.list_phrase = list_phrase
        self.entities = entities
        if self.entities is None:
            self.entities = []
        self.timestamp = datetime.datetime.now()

    def to_tuple(self):
        """

        :return:
        """
        tup = (self.log_id, self.phrase, self.is_list, self.question_phrase, self.list_phrase, self.timestamp)
        return tup

    def add(self):
        """
        add object to log DB
        :return: nothing
        """
        db = MySQLDB.init_db()
        stmt = 'INSERT INTO Logs(log_id, phrase, is_list, question_phrase, list_phrase, timestamp) VALUES' \
               ' (%s, %s, %s, %s, %s, %s)'
        db.insert(stmt, self.to_tuple())
        for entity in self.entities:
            entity.add(db)


class Entity(object):
    """
    entity object database component for logging responses from API
    """
    def __init__(self, log_id, image_id, entity):
        self.entity_id = str(uuid.uuid4())
        self.log_id = log_id
        self.image_id = image_id.replace("https://storage.googleapis.com/livox-images/full/", "")
        self.entity = entity

    def to_tuple(self):
        tup = (self.entity_id, self.log_id, self.image_id, self.entity)
        return tup

    def add(self, db):
        """
        add object to Entity DB
        :return: nothing
        """
        if db is None:
            db = MySQLDB.init_db()
        stmt = 'INSERT INTO Entity(entity_id, log_id, image_id, entity) VALUES (%s, %s, %s, %s)'
        db.insert(stmt, self.to_tuple())