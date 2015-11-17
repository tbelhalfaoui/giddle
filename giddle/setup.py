from peewee import *
from giddle.models import db_element, Question, Answer, RawAnswer


class Setup(object):
    def __init__(self):
        self.tables = [Question, Answer, RawAnswer]

    def drop_tables(self):
        db_element.db.drop_tables(self.tables, safe=True)

    def create_tables(self):
        db_element.db.connect()
        db_element.db.create_tables(self.tables, safe=True)


if __name__ == '__main__':
    raw_input("Warning: all the data from the app will be lost! "+
                "Hit any key to proceed, or ctrl+c to abort.")
    setup = Setup()
    setup.drop_tables()
    print("Tables successfully dropped.")
    setup.create_tables()
    print("Tables successfully created.")