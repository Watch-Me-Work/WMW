import re
import glob
import os
from gensim import corpora, models, similarities
import gensim 

stopwords = [word.strip() for word in open('./stopwords.txt','r').readlines()]
path=os.path.abspath('.')

def read_writeFile(path):
    
    cate=[path+'/'+x for x in os.listdir(path)]
    txt = []
    for idx,folder in enumerate(cate):
        for im in glob.glob(folder+'/*.txt'):
            cur = []
            f1 = open(im, 'r')
            for eachLine in f1:
                cur.append(eachLine)
            f1.close()
            txt.append(cur)
    return txt

def clean_text(text):
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
    for txt in txts:       
        cur = [clean_text(s) for s in txt if len(s) > 0]
        cur = [[word for word in text.lower().split() if word not in stopwords] for text in cur]
        ans = []
        for s in cur:
            ans += s
        cleaned_txt.append(ans)    
    return cleaned_txt


txts = read_writeFile(path)
cleaned_txt = clean_texts(txts)


dictionary = corpora.Dictionary(cleaned_txt)
corpus = [dictionary.doc2bow(text) for text in cleaned_txt]
print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3,passes = 20,iterations = 400)
top_topics = lda.top_topics(corpus)


from pprint import pprint
pprint(top_topics)