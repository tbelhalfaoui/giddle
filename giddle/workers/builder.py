import logging
from giddle.models import Question
from giddle.controllers import AnswersFactory


class Builder(object):
    def __init__(self):
        self.answers_factory = AnswersFactory()

    def run(self):
        while True:
            try:
                question = Question.select().where(Question.processed == False).get()
                question.mark_as_processed()
                logging.info("Processing question '%s'" % question)
            except Question.DoesNotExist as e:
                break

            answers = self.answers_factory.get(question)
            if not answers:
                logging.error("No answers found for question '%s'" % question)
                continue
            for answer in answers:
                answer.save()
            logging.info("Question '%s' processed." % question)
        logging.info("All questions processed.")

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    Builder().run()