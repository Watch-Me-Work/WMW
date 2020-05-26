import collections
import re

import spacy

spacynlp_cache = dict()
def get_spacynlp(model_name, use_cache=True):
    global spacynlp_cache
    if use_cache:
        if model_name not in spacynlp_cache:
            spacynlp_cache[model_name] = spacy.load(model_name)
        return spacynlp_cache[model_name]
    return spacy.load(model_name)

def get_keywords_by_ner(document):
    # Blacklist some things that are never entities (sometimes spacy makes mistakes)
    BLACKLIST = set({'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'first', 'second', 'third'})

    nlp = get_spacynlp('en_core_web_sm')
    spacydoc = nlp(document)
    ent_freqs = collections.Counter()
    keywords = []
    for ent in map(str, spacydoc.ents):
        if ent.lower() in BLACKLIST:
            continue

        if re.match(r'.*[^ a-zA-Z0-9].*', ent) or re.match('[0-9 ]+', ent):
            continue

        ent_freqs[ent] += 1

    keywords = []
    for ent, freq in ent_freqs.items():
        # Prune ents that are just a substring of other ents (note: could have
        # some false prunes if one person's name is a substring of another)
        if any((ent.lower() in ent2.lower()) and (ent != ent2) for ent2 in ent_freqs.keys()):
            continue

        # TODO: Consider pruning low-freq ents (which are more likely to be erroneous)

        keywords.append(ent)

    return sorted(keywords, key=ent_freqs.get, reverse=True)

