import logging
from itertools import chain
from request_maker import RequestMaker, RequestException


class SearchApi(object):
    base_url = 'https://ajax.googleapis.com/ajax/services/search/web'
    page_size = 8
    base_params   = {'v':'1.0', 'rsz':page_size}

    def __init__(self, n_results=8):
        self.n_results = n_results
        self.request_maker = RequestMaker()

    def run(self, query):
        logging.info("Fetching search results for '%s'" % query)
        result_pages = self._fetch_results_all(query)
        pages_formatted = [self._format_result_page(p) for p in result_pages]
        results = list(chain(*pages_formatted))
        logging.info("Retrieved %d search results" % len(results))
        return results

    def _fetch_results_all(self, query):
        pages = [self._fetch_results_one_page(query, start)
                    for start in range(0, self.n_results, self.page_size)]
        full_count = self._get_full_count(pages)
        if full_count:
            logging.info("Search request returned %d results." % full_count)
        else:
            logging.error("Search request returned no result!")
            return []
        return pages

    def _fetch_results_one_page(self, query, start=0):
        params = {'q': query, 'start': start}
        params.update(self.base_params)
        req = self.request_maker.run(self.base_url, params=params)
        if req.status_code != 200:
            raise RequestException("Error during search request '%s'!\n" % query+\
                    "(HTTP status code: %s)" % req.status_code)
        results = req.json()
        google_status_code = results.get('responseStatus')
        if google_status_code != 200:
            raise RequestException("Error during search request '%s'!\n" % query+\
                    "(Google status code: %s)" % google_status_code)
        return req.json()

    def _format_result_page(self, results):
        responseData = results.get('responseData', {})
        raw_results = responseData.get('results', [])
        return [r.get('titleNoFormatting', '')+' '+r.get('content', '')
                            for r in raw_results]

    def _get_full_count(self, result_pages):
        if not result_pages:
            return 0
        responseData = result_pages[0].get('responseData', {})
        count = responseData.get('cursor', {}).get('estimatedResultCount', 0)
        try:
            return int(str(count).replace(',',''))
        except ValueError as e:
            return 0

    def is_empty(self):
        return not bool(self.results)