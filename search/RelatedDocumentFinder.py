import logging
import itertools

from . import search
from .keyword_extraction import get_keywords_by_ner

logging.basicConfig()
logger = logging.getLogger(__name__)

class RelatedDocumentFinder:
    def search(self, document):
        raise NotImplementedError


class NerRelatedDocumentFinder(RelatedDocumentFinder):
    def __init__(self, search_engine):
        self._engine = search_engine

    def search(self, document):
        fulldoc = document.get('body')

        # We set a rough cutoff at 500-1500 characters for a reasonable first paragraph length (about 100-300 words)
        splitpoint = min(max(fulldoc.find('\n\n'), 500), 1500)
        firstsection = fulldoc[:splitpoint]

        # TODO: temporary kludge; should make a better way to upweight firstsection
        ents_sec1 = get_keywords_by_ner(firstsection)
        querystrings = ents_sec1[:1]
        ents_fulldoc = get_keywords_by_ner(fulldoc)
        querystrings += [ent for ent in ents_fulldoc if ent not in querystrings][:3]
        logger.info('Generated querystrings for document: {}. Searching...'.format(str(querystrings)))

        results = []
        # Get results, filtering duplicates along the way
        for res in map(self._engine.search_by_string, querystrings):
            for resitem in res:
                if not any(r.url == resitem.url for r in results):
                    results.append(resitem)
                    break
        return results


class DummyRelatedDocumentFinder(RelatedDocumentFinder):
    """Dummy class for testing.  Always returns the same results."""
    def __init__(self):
        self._engine = DummySearchEngine()

    def search(self, document):
        return self._engine.search_by_string("")

