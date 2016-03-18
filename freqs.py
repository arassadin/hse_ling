import nltk
from nltk.probability import FreqDist

def get_ngrams_with_frequencies(n_grams):
	freqs_file = open('freq.txt', 'a')
	freqs_file.truncate(0)
	for freq in nltk.FreqDist(n_grams).most_common():
		n_gram = ''
		for i in range(0, len(freq[0])):
			n_gram += freq[0][i] + ' '
		print( n_gram, freq [1], file=freqs_file)
	freqs_file.close()
