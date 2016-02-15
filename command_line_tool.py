#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt,sys
sys.path.append("/home/artsokol/anaconda/lib/python2.7/site-packages")
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

def main():
    if sys.version_info < (3, 0):
        print ("must use python 3.0 or greater")
        sys.exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:c", ["help", "corpus="])   
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        get_usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            get_usage()
            sys.exit()
        elif o in ("-c", "--corpus"):
            if a == "":
                get_usage()
                sys.exit()

            input_period = a
        else:
            assert False, "unhandled option"

def get_nGramsTemplate(stringToParse):
    return list(stringToParse.upper().split('+'))

def get_help():
    print("Show n-gramms in corpus:")
    print("Command sequence:")
    print("  WORD1+WORD2+...WORDn")
    print("Alowed words for sequence:")
    print("  СУЩ, ГЛ, ПРИЛ, Н, ПРИЧ, ДЕЕПР, ЧИСЛ")
    print("Example:")
    print("  инф+прил+сущ")
    print("  ГЛ+СУЩ")
    print("exit - terminal closing")
    print("help - show this info")

def get_usage():
    print("Usage:")
    print("cli_tool args") 
    print("-c year_begin-year_end Mnadatory parameter. Certain time period shoud be specifyed")
    print("-h get usage info")
    print("")
    print("--corpus=year_begin-year_end")
    print("--help the same as -h")

if __name__ == "__main__":
    input_period=None
    main()

    #if len (sys.argv) > 1: 
        #data preparing 
    corp = corpus.corpus()
    corp.load('dumps/corp.dump')
#period=[2001-2005]
    data = corp.get_lemm([1997-2010])
    morph = pymorphy2.MorphAnalyzer()

    print("Enter n-gramm sequence or help")
    while 1:
        command = input('--> ')
        if command == "help":
            get_help()
        elif command == "exit":
            sys.exit()
        elif command == "":
            continue
        else:
            #TODO word checking
            ngram_list = get_nGramsTemplate(command)
   
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

