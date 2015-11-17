import unicodedata
import re
from Stemmer import Stemmer


STOP_WORDS = set([u'au', u'aux', u'avec', u'ce', u'ces', u'dans', u'de', u'des', 
                u'du', u'elle', u'en', u'et', u'eux', u'il', u'je', u'la',
                u'le', u'leur', u'les', u'lui', u'ma', u'mais', u'me', u'm\xeame',
                u'mes', u'moi', u'mon', u'ne', u'nos', u'notre', u'nous',
                u'on', u'ou', u'par', u'pas', u'pour', u'qu', u'que', u'qui',
                u'sa', u'se', u'ses', u'son', u'sur', u'ta', u'te', u'tes',
                u'toi', u'ton', u'tu', u'un', u'une', u'vos', u'votre',
                u'vous', u'c', u'd', u'j', u'l', u'\xe0', u'm', u'n', u's',
                u't', u'y', u'\xe9t\xe9', u'\xe9t\xe9e', u'\xe9t\xe9es',
                u'\xe9t\xe9s', u'\xe9tant', u'\xe9tante', u'\xe9tants',
                u'\xe9tantes', u'suis', u'es', u'est', u'sommes', u'\xeates',
                u'sont', u'serai', u'seras', u'sera', u'serons', u'serez',
                u'seront', u'serais', u'serait', u'serions', u'seriez',
                u'seraient', u'\xe9tais', u'\xe9tait', u'\xe9tions',
                u'\xe9tiez', u'\xe9taient', u'fus', u'fut', u'f\xfbmes', 
                u'f\xfbtes', u'furent', u'sois', u'soit', u'soyons', u'soyez',
                u'soient', u'fusse', u'fusses', u'f\xfbt', u'fussions',
                u'fussiez', u'fussent', u'ayant', u'ayante', u'ayantes',
                u'ayants', u'eu', u'eue', u'eues', u'eus', u'ai', u'as',
                u'avons', u'avez', u'ont', u'aurai', u'auras', u'aura',
                u'aurons', u'aurez', u'auront', u'aurais', u'aurait',
                u'aurions', u'auriez', u'auraient', u'avais', u'avait',
                u'avions', u'aviez', u'avaient', u'eut', u'e\xfbmes',
                u'e\xfbtes', u'eurent', u'aie', u'aies', u'ait', u'ayons',
                u'ayez', u'aient', u'eusse', u'eusses', u'e\xfbt',
                u'eussions', u'eussiez', u'eussent'])

def _normalise(word):
    word_u = word if isinstance(word, unicode) else unicode(word, 'utf-8')
    word_nfkd = unicodedata.normalize('NFKD', word_u)
    return word_nfkd.encode('ASCII', 'ignore')

def _tokenise(sentence, min_token_length=1, normalise=True,
                            remove_stop_words=False, stemmer=False):
    regexp = '(?u)\w{%d}\w*' % min_token_length
    tokens = re.findall(regexp, sentence, flags=re.IGNORECASE)
    if normalise:
        tokens = [_normalise(t) for t in tokens]
    if remove_stop_words:
        tokens = filter(lambda t: t not in STOP_WORDS, tokens)
    if stemmer:
        stem = Stemmer('french').stemWord
        tokens = [stem(t) for t in tokens]
    return tokens

def tokenise(sentence, clean):
    return _tokenise(sentence, min_token_length=3 if clean else 1,
                normalise=clean, remove_stop_words=clean, stemmer=clean)

def get_tokeniser(clean):
    return lambda x: _tokenise(x, clean)

def case_insensitive_string_equals(str1, str2):
    return str1.lower() == str2.lower()

def case_insensitive_list_equals(list1, list2):
    return len(list1) == len(list2) and \
            all(case_insensitive_string_equals(str1, str2)
                for str1, str2 in zip(list1, list2))

def word_count(phrase, clean=False):
    tokenise = get_tokeniser(clean)
    return len(set(tokenise(phrase)))