from giddle.controllers import RawAnswersFactory
from giddle.models import RawAnswer, Question


class TestRawAnswersFactory(object):
    @classmethod
    def setup_class(self):
        self.question = Question(query="quel est le plus")
        self.raw_answers = RawAnswersFactory().get(self.question)

    def test_got_a_list_of_raw_answers(self):
        assert isinstance(self.raw_answers, list) \
            and all(isinstance(ra, RawAnswer) for ra in self.raw_answers)

    def test_at_leat_6_results(self):
        assert len(self.raw_answers) >= 6

    def test_all_raw_answers_have_nonempty_phrase(self):
        assert all(ra.phrase for ra in self.raw_answers)

    def test_all_raw_answers_have_nonempty_question(self):
        assert all(ra.question for ra in self.raw_answers)

    def test_all_raw_answers_have_at_least_6_search_results(self):
        assert all(len(ra.search_results) >= 6 for ra in self.raw_answers)
