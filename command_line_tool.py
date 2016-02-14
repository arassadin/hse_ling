#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
#sys.path.append("/home/artsokol/anaconda/lib/python2.7/site-packages")
import pymorphy2
import corpus

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.util import ngrams
from nltk import bigrams


noun="СУЩ"
verb1="ГЛ"
verb2="ИНФ"
adj="ПРИЛ"

def get_nGramsTemplate(stringToParse):
    return list(stringToParse.upper().split('+'))

def get_help():
    print("Usage:")
    print("  Alowed words:")
    print("    СУЩ, ГЛ, ПРИЛ, Н, ПРИЧ, ДЕЕПР, ЧИСЛ")
    print("  Alowed form:")
    print("    WORD1+WORD2+...WORDn")
    print("  Example:")
    print("    инф+прил+сущ")
    print("    ГЛ+СУЩ")
    print("")

if __name__ == "__main__":
    if sys.version_info < (3, 0):
        print ("must use python 3.0 or greater")
        quit()
    if len (sys.argv) > 1: 
        #data preparing 
        morph = pymorphy2.MorphAnalyzer()
        corp = corpus.corpus()
        corp.load('dumps/corp.dump')
        #corp.get_info()
        data = corp.get_lemm(period=[2001, 2005])
        #print (lemmas)
        ngram_list = get_nGramsTemplate(sys.argv[1])
       
        n_grams = ngrams(data, ngram_list.__len__())

        for grams in n_grams:
            i = 0
            for item in grams:
                if (morph.parse(item)[0].tag.POS == None) or \
                   ((ngram_list[i] != morph.lat2cyr(morph.parse(item)[0].tag.POS)) and not (ngram_list[i] == verb1 and morph.lat2cyr(morph.parse(item)[0].tag.POS) == verb2)):
                    break #
                i += 1
            #print if every item is equal
            if i == ngram_list.__len__():
                print(grams)
    else:
        get_help()
        quit()
