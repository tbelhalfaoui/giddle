import logging
import warnings
from operator import itemgetter
from collections import OrderedDict
from itertools import chain, groupby
from math import exp
import random
import numpy as np
from scipy.sparse import vstack
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from ..lib import text
from ..models import Answer
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class AnswersFactory(object):
    threshold = .01
    alpha     = .2
    n_answers = 8

    def get(self, question):
        raw_answers = self._filter_raw_answers(question.raw_answers)
        if not raw_answers:
            return []
        search_matrix, vocab = self._vectorise(question.raw_answers)
        cluster_ids = self._aggregate(search_matrix)
        wordlists = self._answer_wordlists(search_matrix, vocab)
        
        return [Answer(
                    question=question,
                    meta_answer_id=mai,
                    phrase=ra.phrase,
                    keywords=kw
        ) for ra, mai, kw in zip(question.raw_answers, cluster_ids, wordlists)]

    def _filter_raw_answers(self, raw_answers):
        return filter(lambda ra: any(ra.search_results), raw_answers)

    def _vectorise(self, raw_answers):
        results_flat = [''.join(chain(ra.search_results)) for ra in raw_answers]
        vec = TfidfVectorizer(
                    tokenizer=text.get_tokeniser(clean=True),
                    use_idf=False,
                    norm='l2',
                    lowercase=True
        )
        vec.fit(results_flat)
        result_matrices = [self._vectorise_one_raw_answer(ra, vec)
                                    for ra in raw_answers]
        vocabulary = [w for w,_ in
                        sorted(vec.vocabulary_.items(), key=itemgetter(0))]
        return vstack(result_matrices).tocsr(), vocabulary

    def _answer_wordlists(self, search_matrix, vocabulary):
        wordlists = [[(vocabulary[j], row[0,j]) for j in row.indices]
                                for row in search_matrix]
        wordlists_sorted = [OrderedDict(sorted(wordlist, key=itemgetter(1),
                                    reverse=True)) for wordlist in wordlists]
        return wordlists_sorted

    def _vectorise_one_raw_answer(self, raw_answer, vec):
        result_matrices = [exp(-self.alpha*i)*vec.transform([r])
                                for i,r in enumerate(raw_answer.search_results)]
        vector = sum(result_matrices)
        return vector / vector.sum()

    def _aggregate(self, search_matrix):
        cls = KMeans(n_clusters=self.n_answers)
        cluster_ids = cls.fit_predict(search_matrix)
        return cluster_ids
        