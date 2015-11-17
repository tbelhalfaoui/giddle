import json
from peewee import *
from playhouse.postgres_ext import *
from db_element import DBElement
from question import Question


class Answer(DBElement):
    question = ForeignKeyField(Question, related_name='answers')
    meta_answer_id = IntegerField()
    phrase = CharField()
    keywords = JSONField()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.phrase