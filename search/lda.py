import re
import os
from gensim import corpora, models
import gensim 
import pandas as pd
import numpy as np
from nltk.stem import WordNetLemmatizer

stopwords = [word.strip() for word in open('./stopwords.txt','r').readlines()]
path = os.getcwd()
middatafolder = path + os.sep + 'middata' + os.sep



def read_testFile(name):

    f = open(name, encoding='UTF-8')
    lines = f.read()
    res = []
    input = []
    input.append(lines)
    res.append(input)
    f.close()
    return res

def read_csvfile(rows = None):
    
    data = pd.read_csv('mendel_02.topic.csv',nrows =rows, usecols=[28])
    print('data shape:' + str(data.shape))
    raw_data = np.array(data)
    raw_data_list=raw_data.tolist()
    
    return raw_data_list

def make_bigrams(texts):
    
    bigram = gensim.models.Phrases(texts, min_count=3, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    
    return [bigram_mod[doc] for doc in texts]


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


def clean_texts(txts):
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
    Required LDA model files include dictionary.dictionary, lda.model, lda.model.expElogbeta.npy, lda.model.id2word, lda.model.state, lda.model.state.sstats.npy
    They are stored in the file named middata
    Returns a list countained topics sorted by topic relevance
    '''
    
    print('training document....')
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
    
    print('topics generated! ')
    
    return predicted_topics


if __name__ == "__main__":
    
    X = 2 # 1 means training, 2 means prediction
    
    if X == 1:    
        #### LDA training  
        corpusCreated = True # have to create corpus for the first time       
        training_files_number = None # None means training all data
        if not corpusCreated:
            print('create corpus....')
            rawdata = read_csvfile(training_files_number)
            cleaned_txt = clean_texts(rawdata)            
            dictionary = corpora.Dictionary(cleaned_txt)
            dictionary.save(middatafolder + 'dictionary.dictionary')            
            corpus = [dictionary.doc2bow(text) for text in cleaned_txt]
            corpora.MmCorpus.serialize(middatafolder + 'corpus.mm', corpus)
        else:
            print('load corpus....')
            corpus_path = middatafolder + 'corpus.mm'
            dictionary_path = middatafolder + 'dictionary.dictionary'
            corpus = corpora.MmCorpus(corpus_path)
            dictionary = corpora.Dictionary.load(dictionary_path)
        num_topic = len(corpus) // 400
        
        
        print('Number of unique tokens: %d' % len(dictionary))
        print('Number of documents: %d' % len(corpus))       
        print('Number of trained topics: ' + str(num_topic))
        print('start training LDA....')
        lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics = num_topic,update_every=1, passes=2,chunksize = 10000)
        lda.save('lda.model')
        top_topics = lda.top_topics(corpus)
    elif X == 2:
        output = LDAtraining(DocumentName = "test_article.txt")
        print(output)
