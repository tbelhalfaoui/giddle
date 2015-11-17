import logging
from operator import itemgetter
from peewee import *
from playhouse.postgres_ext import *
from db_element import DBElement
from question import Question
from ..lib import text


class RawAnswer(DBElement):
    question = ForeignKeyField(Question, related_name='raw_answers')
    phrase = CharField()
    search_results = ArrayField(TextField)

    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return phrase
