import logging
import requests
from collections import OrderedDict
import operator as op
from ..lib import text
from ..controllers.request_maker import RequestMaker, RequestException


class AutocompleteApi(object):
    base_url    = 'http://suggestqueries.google.com/complete/search'
    base_params = {'client': 'firefox'}
    
    def __init__(self, n_secondary_results=0):
        self.n_secondary_results = n_secondary_results
        self.request_maker = RequestMaker()
        self.tokenise    = text.get_tokeniser(clean=False)

    def run(self, query):
        logging.info("Fetching autocomplete results for '%s'" % query)
        results_raw = self._fetch_results(query)
        results = self._filter_results(results_raw, query)
        logging.info("Retrieved %d suggestions" % len(results))
        return results

    def _fetch_results(self, query):
        results = self._execute_query(query)
        subqueries = self._generate_subqueries(query, results)
        if not self.n_secondary_results:
            return results
        for subquery in subqueries:
            new_results = self._execute_query(subquery)
            new_results_filtered = filter(lambda x: x not in results,
                                                    new_results)
            if new_results_filtered:
                results += filter(lambda x: x not in results,
                            new_results_filtered)[0:self.n_secondary_results]
        return results

    def _generate_subqueries(self, query, results):
        query_n_words = len(self.tokenise(query))
        resultset_words = [self.tokenise(result)
                                        for result in results]
        subqueries = set(' '.join(r[0:query_n_words+2]) for r in resultset_words)
        return subqueries

    def _execute_query(self, query):
        params = {'q': query}
        params.update(self.base_params)
        req = self.request_maker.run(self.base_url, params=params)
        if req.status_code != requests.codes.ok:
            raise RequestException("Error while executing autocomplete request %s"+\
                    "(status code: %s)" % (query, req.status_code))
        return req.json()[1]

    # Filter out the results that does not stricly begin with the query
    # and truncate each result to remove the query
    def _filter_results(self, raw_results, query):
        results_words = [self.tokenise(r) for r in raw_results]
        query_words = self.tokenise(query)
        filter_func = lambda x: \
                        text.case_insensitive_list_equals(
                            x[0:len(query_words)],
                            query_words
                        ) \
                        and len(x)>len(query_words)
        filtered_results_words = filter(filter_func, results_words)
        return [' '.join(frw[len(query_words):])
                            for frw in filtered_results_words]
