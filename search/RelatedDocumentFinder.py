import logging
import itertools

from . import search
from .keyword_extraction import get_keywords_by_ner, LdaKeywordExtractor

logging.basicConfig()
logger = logging.getLogger(__name__)

class RelatedDocumentFinder:
    def search(self, document):
        raise NotImplementedError

class KeywordExtractionRelatedDocumentFinder(RelatedDocumentFinder):
    def __init__(self, search_engine):
        self._engine = search_engine

    def generate_querystrings(self, document, max_strings):
        raise NotImplementedError

    def search(self, document, max_results=4):
        querystrings = self.generate_querystrings(document, max_results)
        logger.info('Generated querystrings: {}'.format(str(querystrings)))

        results = []
        # Get results, filtering duplicates along the way
        for res in map(self._engine.search_by_string, querystrings):
            for resitem in res:
                if not any(r.url == resitem.url for r in results):
                    results.append(resitem)
                    break
        return results

class TopicRelatedDocumentFinder(KeywordExtractionRelatedDocumentFinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keyword_extractor = LdaKeywordExtractor()

    def generate_querystrings(self, document, max_strings):
        fulldoc = document.get('body')
        ents_fulldoc = self._keyword_extractor.get_keywords(fulldoc)
        querystrings = [ent for ent in ents_fulldoc][:max_strings]
        return querystrings

class NerRelatedDocumentFinder(KeywordExtractionRelatedDocumentFinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_querystrings(self, document, max_strings):
        fulldoc = document.get('body')

        firstsection = document.get('first')
        if firstsection is None or len(firstsection) == 0:
            # We set a rough cutoff at 500-1500 characters for a reasonable
            # first paragraph length (about 100-300 words)
            splitpoint = min(max(fulldoc.find('\n\n'), 500), 1500)
            firstsection = fulldoc[:splitpoint]

        # TODO: temporary kludge; should make a better way to upweight firstsection
        ents_sec1 = get_keywords_by_ner(firstsection)
        querystrings = ents_sec1[:1]
        ents_fulldoc = get_keywords_by_ner(fulldoc)
        querystrings += [ent for ent in ents_fulldoc if ent not in querystrings][:(max_strings-1)]
        return querystrings


class DummyRelatedDocumentFinder(RelatedDocumentFinder):
    """Dummy class for testing.  Always returns the same results."""
    def __init__(self):
        self._engine = DummySearchEngine()

    def search(self, document):
        return self._engine.search_by_string("")

