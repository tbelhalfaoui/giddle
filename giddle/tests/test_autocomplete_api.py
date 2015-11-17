from giddle.controllers import AutocompleteApi


class TestAutocompleteApi(object):
    @classmethod
    def setup_class(self):
        self.results = AutocompleteApi().run("comment peut-on")

    def test_returned_a_list(self):
        assert isinstance(self.results, list)

    def test_returned_at_least_6_results(self):
        assert len(self.results) >= 6

    def test_all_results_are_nonempty_strings(self):
        assert all(isinstance(r, basestring) and r for r in self.results)
        