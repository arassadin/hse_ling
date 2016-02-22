#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import sys

# keep for my env compatibility
sys.path.append("/home/artsokol/anaconda/lib/python2.7/site-packages")

import pymorphy2
import corpus
from nltk.util import ngrams


noun = "СУЩ"
verb1 = "ГЛ"
verb2 = "ИНФ"
adj = "ПРИЛ"


def get_options(a_period,a_output=None,a_source=None):
    if sys.version_info < (3, 0):
        print ("must use python 3.0 or greater")
        sys.exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hocs:", ["help", "output=","corpus=","source="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            if a == "":
                usage()
                sys.exit()
            a_output.append(a)
        elif o in ("-c", "--corpus"):
            if a == "":
                usage()
                sys.exit()
            a_period.append(a.split(','))
        elif o in ("-s", "--source"):
            if a == "":
                usage()
                sys.exit()
            a_source.append(a)
            print (a_source)
        else:
            assert False, "unhandled option"

    if a_period==[]:
        usage()
        sys.exit() 

def print_out(data,outfile=None):
    print(data)
    if outfile != None:
        print(data, file=outfile)  

def get_nGramsTemplate(stringToParse):
    return list(stringToParse.upper().split('+'))


def help():
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


def usage():
    print("NAME:")
    print("\tcli.py - command line tool for corpus management")
    print("SYNOPSIS:")
    print("\tcli.py -c first_year,last_year [options]")
    print("OPTIONS:")
    print("\t-c first_year,last_year, --corpus=first_year,last_year\t\tMandatory parameter. Certain time period shoud be specifyed")
    print("\t-h, --help\t\t\t\t\t\t\tGet usage info")
    print("\t-o file, --output=file\t\t\t\t\t\tOutput all information into file")    
    print("\t-s name1,name2,..nameN, --source=name1,name2,..nameN\t\tSpecifies the corpus source newspaper. Valid sources are RG, Novaya")
    print("\t\t\t\t\t\t\t\t\tWithout key all possible sources are used")
    print("")


if __name__ == "__main__":
    input_period = []
    output = []
    newspaper = []
    output_file = None
    get_options(a_period=input_period,a_output=output,a_source=newspaper)

    # data preparing
    if output != []:
        output_file = open(output[0], 'w')

    corp = corpus.corpus()
    corp.load('dumps/corp_multy-lemm.dump')


    #TODO check periods for int
    data = corp.get_lemm(
        period=[int(input_period[0][0]), int(input_period[0][1])],sources=newspaper)
    morph = pymorphy2.MorphAnalyzer()

    print_out("Enter n-gramm sequence or help",output_file)
    #corp.get_info()
    while 1:
        command = input('--> ')
        if command == "help":
            help()
        elif command == "exit":
            if output != []:
                output_file.close()
            sys.exit()
        elif command == "":
            continue
        else:
            # TODO word checking
            ngram_list = get_nGramsTemplate(command)
            
            print_out(ngram_list,output_file)

            n_grams = ngrams(data, ngram_list.__len__())

            for grams in n_grams:
                i = 0

                for item in grams:
                    if (
                        morph.parse(item)[0].tag.POS is None) or (
                        (
                            ngram_list[i] != morph.lat2cyr
                            (
                                morph.parse(item)[0].tag.POS
                            )
                        ) and not (ngram_list[i] == verb1 and morph.lat2cyr(morph.parse(item)[0].tag.POS) == verb2
                                   )
                    ):
                        break
                    i += 1

                # print if every item is equal
                if i == ngram_list.__len__():
                    print_out(grams,output_file)

            print_out("",output_file)
