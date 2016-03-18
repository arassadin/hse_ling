def print_out(what_to_write, where_to_write="", what_to_find=""):
	if where_to_write != "":
		f = open(where_to_write, "w")
		print (what_to_find, file=f)
	counter = 0
	for i, j in sorted(what_to_write.items(), key=lambda item: item[1], reverse=True):
		if i.find('_') != -1:
			if where_to_write == "":
				print (i.split("_")[0], i.split("_")[1], j)
			else:
				print (i.split("_")[0], i.split("_")[1], j, file=f)
		else:
			if where_to_write == "":
				print (i, j)
			else:
				print (i, j, file=f)
		counter+=1
		if counter > 2 and where_to_write == "":
			break
	if where_to_write != "":
		f.close()


def find_collocations(lemmas, what_to_find, output_file="collocation.txt"):
	num_of_word = 0
	length = len(what_to_find)
	stat_left = {}
	stat_right = {}
	stat_both = {}
	for i in range(1, len(lemmas)-1):
		if lemmas[i] == what_to_find[num_of_word]:
			num_of_word+=1
		if num_of_word == length:
			num_of_word = 0
			try:
				stat_left[lemmas[i-length]] += 1
			except:
				stat_left[lemmas[i-length]] = 1
			try:
				stat_right[lemmas[i+1]] += 1
			except:
				stat_right[lemmas[i+1]] = 1
			try:
				stat_both[lemmas[i-length]+"_"+lemmas[i+1]] += 1
			except:
				stat_both[lemmas[i-length]+"_"+lemmas[i+1]] = 1

	print ("hi")
	if output_file == "" or output_file == "collocation.txt":
		print ("\nBefore the ngram:")
		print_out(stat_left)
		print ("\nAfter the ngram:")
		print_out(stat_right)
		print ("\nBefore and after the ngram:")
		print_out(stat_both)
		print ("")
	if output_file != "":
		print_out(stat_left, "left_"+output_file, what_to_find)
		print_out(stat_right, "right_"+output_file, what_to_find)
		print_out(stat_both, "both_"+output_file, what_to_find)
	return stat_left, stat_right, stat_both
