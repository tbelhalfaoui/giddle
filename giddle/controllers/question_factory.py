import random
from ..models import Question

class QuestionFactory(object):
    static_queries_list = [
        "pourquoi les hommes",
        "pourquoi les femmes",
        "combien de temps faut-il pour",
        "Quel est le plus",
        "Comment peut-on",
        "dans quel pays y a-t-il"
    ]

    def __init__(self):
        pass

    def get(self):
        query = random.choice(self.static_queries_list)
        return Question(query=query.capitalize())