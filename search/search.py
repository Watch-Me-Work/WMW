import os
import requests
import lxml.etree


class FoundDocument:
    def __init__(self, title, url=None, snippet=None):
        self.title = title
        self.url = url
        self.snippet = snippet

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_snippet(self):
        return self.snippet


class BingSearchEngine:
    def __init__(self):
        self._subscription_key = os.environ['BING_KEY']
        self._endpoint = 'https://watchmework.cognitiveservices.azure.com/bing/v7.0/search'

    def search_by_string(self, query_string):
        params = { 'q': query_string, 'mkt': 'en-US' }
        headers = { 'Ocp-Apim-Subscription-Key': self._subscription_key }

        try:
            response = requests.get(self._endpoint, headers=headers, params=params)
            response.raise_for_status()
            found_documents = []
            for result in response.json()['webPages']['value']:
                found_documents.append(FoundDocument(result['name'], url=result['url'], snippet=result['snippet']))
            return found_documents
        except Exception as ex:
            raise ex

class WikipediaSearchEngine:
    def __init__(self):
        self._endpoint = 'https://en.wikipedia.org/w/api.php'

    def search_by_string(self, query_string):
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query_string,
            'maxlag': 3,
        }
        headers = { 'User-Agent': f'WatchMeWork/0.1 (m.m.darcy@u.northwestern.edu) Python requests/{requests.__version__}'}

        try:
            response = requests.get(self._endpoint, headers=headers, params=params)
            response.raise_for_status()
            found_documents = []
            for result in response.json()['query']['search']:
                url = f'https://en.wikipedia.org/?curid={result["pageid"]}'
                snippet = ''.join(lxml.etree.fromstring('<span>' + result['snippet'] + '</span>').itertext())
                found_documents.append(FoundDocument(result['title'], url=url, snippet=snippet))
            return found_documents
        except Exception as ex:
            raise ex

class DummySearchEngine:
    def __init__(self):
        pass

    def search_by_string(self, query_string):
        titles_const = ['Southern Hemisphere - Wikipedia', 'The Differences Between Northern & Southern Hemisphere ...', 'Geography of the Southern Hemisphere and Facts', 'Which Countries Are in the Southern Hemisphere ...', 'Countries Located Completely in the Southern Hemisphere ...', "A Beginner's Guide to the Southern Hemisphere Sky - Sky ...", 'Are we prepared for COVID-19 hitting the southern hemisphere?', 'Southern Hemisphere | Definition of Southern Hemisphere by ...', 'Southern hemisphere | Definition of Southern hemisphere at ...', 'Southern Constellations – Constellation Guide'] 
        return [FoundDocument(title) for title in titles_const]


class CorpusSearchEngine:
    def __init__(self, vectorize_fn='lsi'):
        import gensim
        self._vectorize_fn = vectorize_fn
        self._corpus = self.corpus_loader()
        self._corpuslist = ['psyonix', 'codwarzone', 'lastofus', 'larianstudios']
        self._founddocs = []
        if self._vectorize_fn == "lsi":
            self.corpus_bow()
       # if vec_func == tfidf
       # corpus = ...

    def corpus_loader(self):
        docs = [open('wiki/psyonix.txt', 'r').read(), open('wiki/cod-warzone.txt', 'r').read(), open('wiki/last-of-us-2.txt', 'r').read(), open('wiki/larian-studios.txt', 'r').read()]
        for doc in docs:
            doc.replace("\n", " ")
        return docs

    def corpus_bow(self):
        from gensim.utils import simple_preprocess
        from gensim import corpora
        tokenizer = [simple_preprocess(doc) for doc in self._corpus]
        corpusbow = corpora.Dictionary()
        self._corpus = [corpusbow.doc2bow(doc, allow_update=True) for doc in tokenizer]

    def search_by_string(self, string):
        if self._vectorize_fn == "lsi":
            from gensim import models, similarities, corpora
            lsi = models.LsiModel(self._corpus)
            index = similarities.MatrixSimilarity(lsi[self._corpus])
            vec_bow = corpora.Dictionary().doc2bow(string.lower().split())
            vec_lsi = lsi[vec_bow]
            sims = index[vec_lsi]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            for i in range(3):
                title = self._corpuslist[sims[i][0]]
                doc = FoundDocument(title)
                self._founddocs.append(doc)
            return self._founddocs
