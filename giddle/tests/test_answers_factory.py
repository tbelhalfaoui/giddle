from giddle.models import Question, PlayedQuestion, Answer
from giddle.controllers import AnswersFactory

class TestAnswersFactory(object):
    @classmethod
    def setup_class(self):
        self.question = Question(query="pourquoi les francais")
        lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\
            Donec a blandit sem. Phasellus porttitor nunc tortor, sit amet \
            consectetur nisi vulputate id."
        self.raw_answers = [
                Answer(phrase="sont nuls en anglais"),
                Answer(phrase="sont mauvais en anglais"),
                Answer(phrase="parlent mal anglais"),
                Answer(phrase="quittent la france"),
                Answer(phrase="partent de france"),
                Answer(phrase="sont les meilleurs"),
                Answer(phrase="mangent de la baguette"),
                Answer(phrase="boivent du vin"),
            ]
        for ra in self.raw_answers:
            ra.search_results = [lorem_ipsum]*6
            ra.question = self.question
        self.question.raw_answers = self.raw_answers
        self.answers_factory = AnswersFactory()

    @property
    def answers(self):
        return self.answers_factory.get(self.question)

    def test_got_some_answers(self):
        assert self.answers

    def test_got_as_many_answers_as_initial_raw_answers(self):
        assert len(self.answers) == len(self.raw_answers)

    def test_each_answer_has_correct_phrase(self):
        assert set(a.phrase for a in self.answers) == \
                    set(ra.phrase for ra in self.raw_answers)

    def test_each_answer_has_correct_question(self):
        assert set(a.question for a in self.answers) == \
                    set(ra.question for ra in self.raw_answers)

    def test_each_answer_has_nonnegative_meta_answer_id(self):
        assert all(a.meta_answer_id >= 0 for a in self.answers)

    def test_each_answer_has_keywords_with_nonnegative_weights(self):
        assert all(
                all(isinstance(k[0], basestring) and k[1] >= 0
                                            for k in a.keywords.iteritems())
                for a in self.answers)
