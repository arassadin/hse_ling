#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import sys

# keep for my env compatibility
sys.path.append("/home/artsokol/anaconda/lib/python2.7/site-packages")

import pymorphy2
import corpus
import collocation
import find_by_mask
from nltk.util import ngrams
import freqs

noun = "СУЩ"
verb1 = "ГЛ"
verb2 = "ИНФ"
adj = "ПРИЛ"


def get_options(a_period,a_output=None,a_source=None):
    if sys.version_info < (3, 0):
        print ("must use python 3.0 or greater")
        sys.exit()
    try:
        #opts, args = getopt.getopt(sys.argv[1:], "hocs:", ["help", "output=","corpus=","source="])
        opts, args = getopt.getopt(sys.argv[1:], "hocs:", ["help", "corpus=","source="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
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
    print ("choice action:")
    print ("collocation <ngram_with_spaces> - find all collocations for the ngram,\n"
           "    save into *_collocation.txt files\n"
           "    and output three the most common collocations")
    print ("mask_search <file_name> - find all phrases according its mask\n"
           "    defined by parts of speech\n"
           "    and save into <file_name> file (stdout by default)\n"
           "    <file_name> is optional")
    print ("freq <n for ngrams> - count frequencies for all ngrams\n"
           "    and save it into freq.txt file\n"
           "    n can be from 1 to 3")
    #print ("sentiment - output in file sorted text sentiments for the chosen corpus")
    print ("help - for help")
    print ("exit - for exit")

def usage():
    print("NAME:")
    print("\tcli.py - command line tool for corpus management")
    print("SYNOPSIS:")
    print("\tcli.py -c first_year,last_year [options]")
    print("OPTIONS:")
    print("\t-c first_year,last_year, --corpus=first_year,last_year\t\tMandatory parameter. Certain time period shoud be specifyed")
    print("\t-h, --help\t\t\t\t\t\t\tGet usage info")
    #print("\t-o file, --output=file\t\t\t\t\t\tOutput all information into file")
    print("\t-s name1,name2,..nameN, --source=name1,name2,..nameN\t\tSpecifies the corpus source newspaper. Valid sources are RG, Novaya")
    print("\t\t\t\t\t\t\t\t\tWithout key all possible sources are used")
    print("")

if __name__ == "__main__":
    input_period = []
    output = []
    newspaper = []
    output_file = None
    get_options(a_period=input_period,a_output=output,a_source=newspaper)
    corp = corpus.corpus()
    corp.load('dumps/corp_multy-lemm.dump')
    data = corp.get_lemm(period=[int(input_period[0][0]), int(input_period[0][1])], sources=newspaper)
    help()
    while True:
        command = input('--> ')
        if command == "help":
            help()

        elif command[:len("collocation")] == "collocation":
            try:
                command.split(' ')[1]
            except:
                print ("ngram wasn't found")
                help()
                continue
            collocation.find_collocations(data, command.split(' ')[1:])

        elif command[:len("mask_search")] == "mask_search":
            try:
                find_by_mask.find_by_part_of_speech(data, command.split(' ')[1])
            except:
                find_by_mask.find_by_part_of_speech(data)

        elif command[:len("freq")] == "freq":
            try:
                if(int(command.split(' ')[1]) not in range(1,4)):
                    print ("incorrect n for ngrams\n")
                    help()
                    continue
            except:
                print ("incorrect n for ngrams\n")
                help()
                continue
            freqs.get_ngrams_with_frequencies(data, int(command.split(' ')[1]))

        elif command[:len("exit")] == "exit":
            sys.exit()

        elif command[:len("sentiment")] == "sentiment":
            print ("not supported")
            help()

        else:
            print ("incorrect command\n")
            help()

