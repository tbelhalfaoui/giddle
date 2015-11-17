from giddle.models import Question, PlayedQuestion
from giddle.controllers import AnswerEvaluator

class TestAnswerEvaluator(object):
    @classmethod
    def setup_class(self):
        self.question = Question.get_random()
        self.answers = list(self.question.answers)
        self.answer_evaluator = AnswerEvaluator()

    def _evaluate(self, proposal):
        return self.answer_evaluator.evaluate(
                    PlayedQuestion(self.question), proposal)

    def test_all_correct_answers_are_evaluated_as_correct(self):
        assert all(self._evaluate(a.phrase) for a in self.answers)

    def test_a_wrong_answer_is_evaluated_as_wrong(self):
        pass # TODO