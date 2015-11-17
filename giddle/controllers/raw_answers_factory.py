import logging
from autocomplete_api import AutocompleteApi
from search_api import SearchApi
from ..lib import text
from ..models import RawAnswer


class RawAnswersFactory(object):
    n_secondary_results=0
    n_search_results=2

    def __init__(self):
        self.autocomplete_api = AutocompleteApi(
                                n_secondary_results=self.n_secondary_results)
        self.search_api = SearchApi(n_results=self.n_search_results)

    def get(self, question):
        autocomplete_results = self.autocomplete_api.run(question.query)
        search_queries = ["%s %s" % (question.query, s) for s in autocomplete_results]
        search_results = [self.search_api.run(q) for q in search_queries]
        return [RawAnswer(question=question, phrase=p, search_results=sr)
            for p, sr in zip(autocomplete_results, search_results)]
