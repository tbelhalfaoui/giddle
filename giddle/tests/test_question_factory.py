from giddle.models import Question
from giddle.controllers import QuestionFactory


class TestQuestionFactory(object):
    @classmethod
    def setup_class(self):
        pass

    def test_got_some_nonempty_question(self):
        question = QuestionFactory().get()
        assert isinstance(question, Question) and len(question.query) > 0