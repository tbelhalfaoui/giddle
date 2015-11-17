from giddle.controllers import SearchApi


class TestSearchApi(object):
    @classmethod
    def setup_class(self):
        self.results = SearchApi(n_results=8).run("pourquoi les anglais")

    def test_returned_a_list(self):
        assert isinstance(self.results, list)

    def test_returned_8_results(self):
        assert len(self.results) == 8

    def test_all_results_are_nonempty_strings(self):
        assert all(isinstance(r, basestring) and r for r in self.results)
        