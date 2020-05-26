from .search import BingSearchEngine, DummySearchEngine, CorpusSearchEngine
from .keyword_extraction import get_keywords_by_ner

class RelatedDocumentFinder:
    def search(self, document):
        raise NotImplementedError


class BingRelatedDocumentFinder(RelatedDocumentFinder):
    def __init__(self):
        self._engine = BingSearchEngine()

    def search(self, document):
        ents = get_keywords_by_ner(document.get('body'))
        print(document.get('body'))
        querystring = ents[0]
        return self._engine.search_by_string(querystring)

class DummyRelatedDocumentFinder(RelatedDocumentFinder):
    """Dummy class for testing.  Always returns the same results."""
    def __init__(self):
        self._engine = DummySearchEngine()

    def search(self, document):
        return self._engine.search_by_string("")

class CorpusRelatedDocumentFinder(RelatedDocumentFinder):
    def __init__(self):
        self._engine = CorpusSearchEngine()

    def search(self, document):
        return self._engine.search_by_string(document.get('body'))
