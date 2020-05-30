import collections
import re

import spacy

import os
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer

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


###LDA part###

def read_testFile(name):

    f = open(name, encoding='UTF-8')
    lines = f.read()
    res = []
    input = []
    input.append(lines)
    res.append(input)
    f.close()
    return res

def clean_text(text):
    
    text = re.sub("<.*?>", " ", text)  
    text = text.replace('\n'," ")                      
    text = re.sub(r"-", " ", text)                      
    text = re.sub(r"\d+/\d+/\d+", "", text)             
    text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", "", text)  
    text = re.sub(r"[\w]+@[\.\w]+", "", text)           
    text = re.sub(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", text) 
    pure_text = ''
    for letter in text:
        if letter.isalpha() or letter==' ':
            pure_text += letter
            
    text = ' '.join(word for word in pure_text.split() if len(word)>1)

    return text

def make_bigrams(texts):
    
    bigram = gensim.models.Phrases(texts, min_count=3, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    
    return [bigram_mod[doc] for doc in texts]

def clean_texts(txts):
    stopwords = [word.strip() for word in open('./stopwords.txt','r').readlines()]
    cleaned_txt = []
    wnl = WordNetLemmatizer()
    for txt in txts:       
        cur = [clean_text(s) for s in txt if len(s) > 0]
        cur = [[wnl.lemmatize(word) for word in text.lower().split() if word not in stopwords] for text in cur]
        ans = []        
        for s in cur:            
            ans += s   
            
        if len(ans) > 50:
            cleaned_txt.append(ans) 
    cleaned_txt = make_bigrams(cleaned_txt)
    
    return cleaned_txt

def LDAtraining(DocumentName):
    '''
    input is the name of the document like "test_article.txt" ,it is stored in a same directory with py file
    stopword is a txt file which is stored in a same directory with py file
    Required LDA model files include dictionary.dictionary, lda.model, lda.model.expElogbeta.npy, lda.model.id2word, lda.model.state, lda.model.state.sstats.npy
    They are stored in the file named middata in a same directory with py file
    Returns a list countained topic id with words sorted by topic relevance
    '''
    
    path = os.getcwd()
    # file path stores the model files and dictionary 
    middatafolder = path + os.sep + 'middata' + os.sep
    dictionary_path = middatafolder + 'dictionary.dictionary'
    
    # load LDA model and LDA dictionary
    lda = models.ldamodel.LdaModel.load(middatafolder + 'lda.model')    
    dictionary = corpora.Dictionary.load(dictionary_path)
    # document text process and bow generation  
    predict_txt = read_testFile(DocumentName)
    cleaned_txt = clean_texts(predict_txt)
    corpus = [dictionary.doc2bow(text) for text in cleaned_txt]
    
    # topics prediction
    topics = lda.get_document_topics(corpus) 
    
    # generate topics with words in the order of relevance
    res = topics[0]
    res.sort( key = lambda x: - x[1] )  
    matched_ids = []
    
    for item in res:
        matched_ids.append(item[0])
        
    x=lda.show_topics(num_topics = -1,num_words=7,formatted=False)
    topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in x]
    matched_results = {}
    
    for topic,words in topics_words:
        if topic in matched_ids:
            matched_results[topic] = str(words)
            
    predicted_topics = []
    
    for s in matched_ids:
        predicted_topics.append([s,matched_results[s]])
   
    
    return predicted_topics

