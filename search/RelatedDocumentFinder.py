import multiprocessing
import itertools

from .search import BingSearchEngine, DummySearchEngine, CorpusSearchEngine
from .keyword_extraction import get_keywords_by_ner

class RelatedDocumentFinder:
    def search(self, document):
        raise NotImplementedError


class BingRelatedDocumentFinder(RelatedDocumentFinder):
    def __init__(self):
        self._engine = BingSearchEngine()

    def search(self, document):
        fulldoc = document.get('body')

        # We set a rough cutoff at 500-1500 characters for a reasonable first paragraph length (about 100-300 words)
        splitpoint = min(max(fulldoc.find('\n\n'), 500), 1500)
        firstsection = fulldoc[:splitpoint]

        # TODO: temporary kludge; should make a better way to upweight firstsection
        ents_sec1 = get_keywords_by_ner(firstsection)
        querystrings = ents_sec1[:1]
        ents_fulldoc = get_keywords_by_ner(fulldoc)
        querystrings += ents_fulldoc[:3]
        results = []
        with multiprocessing.Pool(1) as pool:
            results = itertools.chain(*[res[:1] for res in pool.imap(self._engine.search_by_string, querystrings)])
        return results

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
