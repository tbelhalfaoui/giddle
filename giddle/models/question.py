from db_element import DBElement
from peewee import *


class Question(DBElement):
    query = CharField(null=False)
    processed = BooleanField(default=False)

    def __str__(self):
        return self.query

    def mark_as_processed(self):
        self.processed = True
        self.save()

    @staticmethod
    def get_random():
        return Question.select().order_by(fn.Random()).get()
