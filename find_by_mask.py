import pymorphy2
from nltk.util import ngrams
import getopt
import sys

noun = "СУЩ"
verb1 = "ГЛ"
verb2 = "ИНФ"
adj = "ПРИЛ"


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


def print_out(data, outfile=None):
	print(data)
	if outfile != None:
		print(data, file=outfile)


def get_nGramsTemplate(stringToParse):
	return list(stringToParse.upper().split('+'))


def find_by_part_of_speech(data, output=""):
	output_file = None
	if output != "":
		output_file = open(output, 'w')
	morph = pymorphy2.MorphAnalyzer()

	print_out("Enter n-gramm sequence or help", output_file)
	# corp.get_info()
	while 1:
		command = input('--> ')
		if command == "help":
			help()
		elif command == "exit":
			if output != "":
				output_file.close()
			sys.exit()
		elif command == "":
			continue
		else:
			# TODO word checking
			ngram_list = get_nGramsTemplate(command)

			print_out(ngram_list, output_file)

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
								) and not (
									ngram_list[i] == verb1 and morph.lat2cyr(morph.parse(item)[0].tag.POS) == verb2
									)
					):
						break
					i += 1

				# print if every item is equal
				if i == ngram_list.__len__():
					print_out(grams, output_file)

			print_out("", output_file)
