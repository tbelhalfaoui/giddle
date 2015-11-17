import time
import logging
from giddle.controllers import QuestionFactory, RawAnswersFactory, RequestException


class Crawler(object):
    waiting_time_on_failure = 10
    max_tries = 10

    def __init__(self, n):
        self.question_factory = QuestionFactory()
        self.raw_answers_factory = RawAnswersFactory()
        self.n = n

    def run(self):
        for i in xrange(self.n):
            question = self.question_factory.get()
            logging.info("Getting question '%s'" % question)
            for _ in xrange(self.max_tries):
                try:
                    raw_answers = self.raw_answers_factory.get(question)
                    question.save()
                    for ra in raw_answers:
                        ra.save()
                    logging.debug("Done")
                    break
                except RequestException as e:
                    logging.exception("Error building '%s'. " % question+\
                      "Retrying in %d seconds." % self.waiting_time_on_failure)
                    time.sleep(self.waiting_time_on_failure)
                except Exception as e:
                    logging.exception("Unable to crawl question '%s'!"
                                                        % question)
        

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    Crawler(n=5).run()