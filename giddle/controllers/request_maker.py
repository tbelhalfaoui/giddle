import time
import random
import logging
import requests
logging.getLogger("requests").setLevel(logging.WARNING)


class RequestMaker(object):
    min_waiting_time = 3
    max_waiting_time = 4
    headers          = {'headers': 'Mozilla/5.0 (Windows; U; '+\
        'Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

    def run(self, *args, **kwargs):
        l = self.max_waiting_time - self.min_waiting_time
        t = self.min_waiting_time + l*random.random()
        time.sleep(t)
        kwargs.update(headers=self.headers)
        return requests.get(*args, **kwargs)


class RequestException(Exception):
    pass