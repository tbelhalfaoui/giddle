from giddle.models import Question, PlayedQuestion, Answer


class TestQuestionFactory(object):
    @classmethod
    def setup_class(self):
        self.question = Question(query="pourquoi les francais")
        self.answers = [
                Answer(phrase="sont nuls en anglais", meta_answer_id="0"),
                Answer(phrase="sont mauvais en anglais", meta_answer_id="0"),
                Answer(phrase="quittent la france", meta_answer_id="1"),
                Answer(phrase="partent de france", meta_answer_id="1"),
                Answer(phrase="sont les meilleurs", meta_answer_id="2"),
            ]
        for a in self.answers:
            a.keywords = []
            a.question = self.question
        self.question.answers = self.answers
        self.played_question = PlayedQuestion(self.question)

    def _assert_state(self, answers_found, remaining_answers, remaining_meta_answers):
        assert self.played_question.answers_found == answers_found
        assert self.played_question.remaining_answers == remaining_answers
        assert self.played_question.remaining_meta_answers == remaining_meta_answers

    def test0_initial_state(self):
        self._assert_state(
            [],
            self.answers,
            [self.answers[1], self.answers[3], self.answers[4]]
        )

    def test1_state_after_one_correct_answer(self):
        self.played_question.add_answer_found(self.answers[2])
        self._assert_state(
            [self.answers[2]],
            [self.answers[0], self.answers[1], self.answers[4]],
            [self.answers[1], self.answers[4]]
        )

    def test2_state_after_two_correct_answers(self):
        self.played_question.add_answer_found(self.answers[1])
        self._assert_state(
            [self.answers[2], self.answers[1]],
            [self.answers[4]],
            [self.answers[4]]
        )

    def test3_final_state(self):
        self.played_question.add_answer_found(self.answers[4])
        self._assert_state(
            [self.answers[2], self.answers[1], self.answers[4]],
            [],
            []
        )  