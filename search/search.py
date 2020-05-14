import os
import requests


class FoundDocument:
    def __init__(self, title):
        self.title = title

    def get_title(self):
        return self.title


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
                found_documents.append(FoundDocument(result['name']))
            return found_documents
        except Exception as ex:
            raise ex



class CorpusSearchEngine:
    def __init__(self, vectorize_fn):
        self._vectorize_fn = vectorize_fn
        self._corpus = self.corpus_loader()
        self._corpuslist = ['psyonix', 'codwarzone', 'lastofus', 'larianstudios']
        if self._vectorize_fn == "lsi":
            self.corpus_bow()
       # if vec_func == tfidf
       # corpus = ...

    def corpus_loader(self):
        from gensim.utils import simple_preprocess
        docs = [open('wiki/psyonix.txt', 'r').read(), open('wiki/cod-warzone.txt', 'r').read(), open('wiki/last-of-us-2.txt', 'r').read(), open('wiki/larian-studios.txt', 'r').read()]
        for doc in docs:
            doc.replace("\n", " ")
        return docs

    def corpus_bow(self):
        from gensim.utils import simple_preprocess
        from gensim import corpora
        tokenizer = [simple_preprocess(doc) for doc in corpus]
        corpusbow = corpora.Dictionary()
        self._corpus = [corpusbow.doc2bow(doc, allow_update=True) for doc in tokenizer]

    def search_by_string(self, string):
        if self._vectorize_fn == "lsi":
            from gensim import models
            from gensim import similarities
            lsi = models.LsiModel(self._corpus)
            index = similarities.MatrixSimilarity(lsi[self._corpus])
            vec_bow = dict.doc2bow(string.lower().split())
            vec_lsi = lsi[vec_bow]
            sims = index[vec_lsi]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            return self._corpuslist[sims[0][0]][0:10]
