from itertools import groupby
from collections import OrderedDict
import random
from ..lib import text


class PlayedQuestion(object):
    def __init__(self, question):
        self.question = question
        self.answers = list(question.answers)
        self._answers_found = OrderedDict() # Key: meta_answer_id, Value: answer

    @property
    def answers_found(self):
        return self._answers_found.values()

    @property
    def remaining_answers(self):
        return filter(lambda a: a.meta_answer_id not in self._answers_found,
            self.answers) 

    @property
    def remaining_meta_answers(self):
        return OrderedDict((a.meta_answer_id, a)
                    for a in self.remaining_answers).values()

    @property
    def hint(self):
        choices = filter(lambda a: text.word_count(a.phrase, clean=False) >= 2,
                                                    self.remaining_answers)
        if not choices:
            return ""
        answer_hint = random.choice(choices)
        return text.tokenise(answer_hint.phrase, clean=False)[0]

    def add_answer_found(self, answer):
        self._answers_found[answer.meta_answer_id] = answer
