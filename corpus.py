import os
import glob
import codecs
import string
import re
import pymorphy2
import pickle
import collections
from operator import itemgetter

EXCLUDE_SYMBOLS = ['№', '«', 'ђ', '°', '±', '‚', 'ћ', '‰', '…',
                   '»', 'ѓ', 'µ', '·', 'ґ', 'њ', 'ї', 'џ', 'є', '‹',
                   '‡', '†', '¶', 'ќ', '€', '“', 'ў', '§', '„', '”',
                   '\ufeff', '’', 'љ', '›', '•', '—', '‘', '\x7f', '\xad', '¤']

EXCLUDE_SYMBOLS_STR = ''
for symb in EXCLUDE_SYMBOLS:
    EXCLUDE_SYMBOLS_STR += str(symb)


class text_unit(object):

    def __init__(self, dates=[], sources=[]):
        self.dates = dates
        self.sources = sources
        self.texts, self.words, self.lemm = [], [], []

    def read(self, root='.', folder='', suffix='*'):
        files = glob.glob(os.path.join(root, folder, suffix))
        regex_punct = re.compile('[%s]' % re.escape(string.punctuation))
        regex_dig = re.compile('[%s]' % re.escape(string.digits))
        regex_symb = re.compile('[%s]' % re.escape(EXCLUDE_SYMBOLS_STR))
        regex_struct = re.compile(
            '[%s]' % string.printable + string.whitespace)

        self.texts = []
        self.words = []
        for f in files:
            with codecs.open(f, 'r', 'utf-8') as text:
                raw_text = text.read()
                filt_text = regex_punct.sub('', raw_text)
                filt_text = regex_dig.sub('', filt_text)
                filt_text = regex_symb.sub('', filt_text)
                filt_text = regex_struct.sub('', filt_text)
                self.texts.append(filt_text)
                self.words += filt_text.split()
            # break

        print ('Read {} texts'.format(len(self.texts)))
        # self.words = set(self.words)
        print ('Total {} unique words'.format(len(self.words)))
        # self.words = [word for word in self.words if len(word) > 2]
        print ('{} words after filtering'.format(len(self.words)))

    def get_lemm(self):
        morph = pymorphy2.MorphAnalyzer()
        self.lemm = []
        for word in self.words:
            if len(word) > 2:
                norm = morph.parse(word)[0].normal_form
                if norm is not '':
                    self.lemm.append(norm)
        print ('Found {} lemmas'.format(len(self.lemm)))

    def get_lemm_unique(self):
        return list(set(self.lemm))

    def dump(self, path='dumps/dump'):
        pickle.dump(self, open(path, 'wb'))

    def load(self, path):
        dump = pickle.load(open(path, 'rb'))
        self.period = dump.period
        self.sources = dump.sources
        self.texts = dump.texts
        self.words = dump.words
        self.lemm = dump.lemm


class corpus(object):

    def __init__(self, entries=[]):
        self.entries = []
        self.lemm, self.dates, self.sources = [], [], []
        self.stats = {}
        if self.entries != []:
            self.update_corpus()

    def update_stat(self):
        self.stats['lemmas'] = {
            'value': self.lemm, 'descr': 'All lemmas in corpus'}
        # TODO on_update for every stat.

    def update_corpus(self):
        for entry in self.entries:
            self.dates += entry.dates
            self.sources += entry.sources
            if entry.lemm == []:
                entry.get_lemm()
            self.lemm += entry.lemm
        self.dates = list(set(self.dates))
        self.sources = list(set(self.sources))
        # self.lemm = list(set(self.lemm))
        self.update_stat()

    def get_lemm(self, sources=None, period=None):
        lemmas = []

        if sources and period:
            for entry in self.entries:

                if len(entry.sources) > len(sources):
                    continue

                self.sources_flag = True
                for source in entry.sources:
                    if source not in sources:
                        self.sources_flag = False
                        break
                if not self.sources_flag:
                    continue

                self.date_flag = True
                for date in entry.dates:
                    if date < period[0] or date > period[1]:
                        self.date_flag = False
                        break
                if not self.date_flag:
                    continue

                if entry.lemm == []:
                    entry.get_lemm()
                lemmas += entry.lemm
            # lemmas = list(set(lemmas))
            print ('{} lemmas selected'.format(len(lemmas)))

        elif sources:
            for entry in self.entries:

                if len(entry.sources) > len(sources):
                    continue

                self.sources_flag = True
                for source in entry.sources:
                    if source not in sources:
                        self.sources_flag = False
                        break
                if not self.sources_flag:
                    continue

                if entry.lemm == []:
                    entry.get_lemm()
                lemmas += entry.lemm
            # lemmas = list(set(lemmas))
            print ('{} lemmas selected'.format(len(lemmas)))

        elif period:
            for entry in self.entries:

                self.date_flag = True
                for date in entry.dates:
                    if date < period[0] or date > period[1]:
                        self.date_flag = False
                        break
                if not self.date_flag:
                    continue

                if entry.lemm == []:
                    entry.get_lemm()
                lemmas += entry.lemm
            # lemmas = list(set(lemmas))
            print ('{} lemmas selected'.format(len(lemmas)))

        else:
            for entry in self.entries:
                if entry.lemm == []:
                    entry.get_lemm()
                lemmas += entry.lemm
            # lemmas = list(set(lemmas))
            print ('{} lemmas selected'.format(len(lemmas)))

        self.lemm = lemmas
        return lemmas

    def get_lemm_freq(self, topq=None, unique=False):
        counter = collections.Counter(self.lemm)
        if topq is None:
            return sorted(zip(self.lemm, counter.values()),
                          key=itemgetter(1), reverse=True)
        else:
            return counter.most_common(topq)

    def get_info(self):
        print ('*** Corpus info: ***')
        print ('{} sources'.format(len(self.sources)))
        print ('{} lemmas'.format(len(self.stats['lemmas']['value'])))
        print ('{} statistics:'.format(len(self.stats)))
        for stat_name, stat in self.stats.items():
            print ('\t{}: {}'.format(stat_name,
                                     stat.get('descr', '--no description--')))
        print ('*** end corpus info ***')

    def add_stat(self, name, value, descr):
        self.stats[name] = {'value': value, 'descr': descr}

    def add(self, entry):
        self.entries.append(entry)
        self.update_corpus()

    def dump(self, path='dumps/dump'):
        pickle.dump(self, open(path, 'wb'))

    def load(self, path):
        dump = pickle.load(open(path, 'rb'))
        self.entries = dump.entries
        self.lemm = dump.lemm
        self.stats = dump.stats
        self.dates = dump.dates
        self.sources = dump.sources
