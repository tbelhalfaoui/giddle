import logging
from operator import itemgetter
from ..lib import text


class AnswerEvaluator(object):
    def __init__(self):
        self.threshold = .01

    def evaluate(self, played_question, proposal):
        answers = filter(lambda a: text.word_count(proposal, clean=True) >=
                            min(text.word_count(a.phrase, clean=True), 2),
                            played_question.remaining_answers)
        if not answers:
            return
        scores = [self._score(proposal, a) for a in answers]
        best_score, best_answer = max(zip(scores, answers), key=itemgetter(0))
        print("Scores = %s" % zip(scores, answers))
        if best_score >= self.threshold:
            played_question.add_answer_found(best_answer)
            return best_answer
        else:
            return

    def _score(self, proposal, answer):
        given_answer_tok = text.tokenise(proposal, clean=True)
        if not given_answer_tok:
            return 0.
        weights = [answer.keywords.get(w, 0.) for w in given_answer_tok]
        score = sum(weights)/float(len(given_answer_tok))
        return all(w > 0 for w in weights)*score
