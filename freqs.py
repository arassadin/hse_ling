import nltk

def get_ngrams_with_frequencies(data, n):
	freqs_file = open('freq.txt', 'w')
	freqs_file.truncate(0)
	freqs_all = nltk.FreqDist(nltk.ngrams(data, n)).most_common()
	for freq in freqs_all:
		print (" ".join(freq[0]), freq[1], file=freqs_file)
	for freq in freqs_all[:10]:
		print (" ".join(freq[0]), freq[1])
	freqs_file.close()
	return freqs_all
