import pandas as pd
import numpy as np
import unicodedata
import re
import nltk
from nltk.corpus import stopwords
from aquire import get_blog_articles, get_all_shorts


def basic_clean(string):
    clean = string.lower()
    clean = unicodedata.normalize('NFKD', clean)\
    .encode('ascii', 'ignore')\
    .decode('utf-8')
    clean = re.sub(r'[^a-z0-9\'\s]', '', clean)
    
    return clean

def tokenize(string):
    toke = nltk.tokenize.ToktokTokenizer()
    toked = toke.tokenize(string, return_str=True)
    return toked

def stem(string):
    ps = nltk.porter.PorterStemmer()
    stemmed = [ps.stem(word) for word in string.split()]
    stemmed = ' '.join(stemmed)
    return stemmed

def lemmatize(string):
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    lemman = [wnl.lemmatize(word) for word in string.split()]
    
    output_lemman = ' '.join(lemman)
    
    return output_lemman

def remove_stopwords(string):
    stopper = stopwords.words('english')
    stopper.append("'")
    my_words = string.split()
    dont_stop = [word for word in my_words if word not in stopper]
    unstopped = ' '.join(dont_stop)
    return unstopped

def make_original(dataframe):
    for i in dataframe:
        if i == 'body':
            dataframe['original'] = dataframe['body'].copy()
            dataframe.drop(columns= 'body', inplace=True)
        if i == 'content':
            dataframe['original'] = dataframe['content'].copy()
            dataframe.drop(columns= 'content', inplace=True)
    return dataframe

def make_clean(dataframe):
    dataframe['clean'] = dataframe['original'].apply(basic_clean).apply(tokenize).apply(remove_stopwords)
    return dataframe

def make_stemmed(dataframe):
    dataframe['stemmed'] = dataframe['clean'].apply(stem)
    return dataframe

def make_lemmatized(dataframe):
    dataframe['lemmatized'] = dataframe['clean'].apply(lemmatize)
    return dataframe

def make_nlp_df():
    '''
    No Parameters:
    --------------
    
    Returns 2 Dataframes:   codeup_df, news_df
    
    Both will contain columns ['title', 'content', 'original', 'clean', 'stemmed', 'lemmatized']
    '''
    codeup_df = get_blog_articles()
    news_df = get_all_shorts()
    
    codeup_df = make_lemmatized(make_stemmed(make_clean(make_original(codeup_df))))
    news_df = make_lemmatized(make_stemmed(make_clean(make_original(news_df))))
    
    return codeup_df, news_df

