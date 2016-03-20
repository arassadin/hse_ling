from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
import os, sys, glob, pickle

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

DATA_DIR = glob.glob(os.path.abspath(os.path.join(os.path.curdir, 'data')))
DUMP_DIR = glob.glob(os.path.abspath(os.path.join(os.path.curdir, 'dumps')))

def calc_sentiments():
	"""for using this func you must exec alchemyapi.py with key
	from api_key.txt as a parameter"""
	path_files = DATA_DIR[0]+ '\\*\\*.txt'
	files = glob.glob(path_files)
	all_tones = []

	print (path_files)
	print (files)
	cur_text = ''
	count = 0
	for filename_txt in files:
		print (filename_txt)
		count+=1
		with open(filename_txt, 'r', encoding="utf8") as f:
			cur_text = f.read().replace('\n', ' ')
		response = alchemyapi.sentiment('text', cur_text)
		if response['status'] == 'OK':
			#print (cur_text)
			#all_tones.append((filename_txt, response['docSentiment']['score']))
			if 'score' in response['docSentiment']:
				all_tones.append((filename_txt, response['docSentiment']['score']))
				print('score: ', response['docSentiment']['score'], "\n")
				pickle.dump(all_tones, open(DUMP_DIR[0]+"\\tones.dump", 'wb'))
			elif response['docSentiment']["type"] == "neutral": # possible
				all_tones.append((filename_txt, 0))
				print('!!!score: ', 0, "\n")
				pickle.dump(all_tones, open(DUMP_DIR[0]+"\\tones.dump", 'wb'))
			elif response['docSentiment']["type"] == "positive": # not possible
				all_tones.append((filename_txt, 1))
				print('!!!score: ', 1, "\n")
				pickle.dump(all_tones, open(DUMP_DIR[0]+"\\tones.dump", 'wb'))
			elif response['docSentiment']["type"] == "negative": # not possible
				all_tones.append((filename_txt, -1))
				print('!!!score: ', -1, "\n")
				pickle.dump(all_tones, open(DUMP_DIR[0]+"\\tones.dump", 'wb'))
			else:
				print ("no type, no score")
		else:
			print('Error in sentiment analysis call: ', response['statusInfo'])

	print (all_tones, count)
	print (DUMP_DIR[0]+"\\tones.dump")
	pickle.dump(all_tones, open(DUMP_DIR[0]+"\\tones.dump", 'wb'))
	#return all_tones

#calc_sentiments()

def ask_sentiment(print_max_min_texts, years=[], sources=[]):
	DATA_DIR = glob.glob(os.path.abspath(os.path.join(os.path.curdir, 'data')))
	DUMP_DIR = glob.glob(os.path.abspath(os.path.join(os.path.curdir, 'dumps')))
	years=years[0]
	# print_max_min_texts - yes(True)
	# process parameters
	sources_etalon = {"Novaya": "nv", "RG": "rg"}
	years_etalon = [1998, 2001, 2004, 2016]
	years_etalon_dict = {1998:"98", 2001:"01", 2004:"04", 2016:"16"}
	text_for_analysis = []
	sources_for_analysis = []
	years_for_analysis = []

	# years
	if years == []:
		years_for_analysis = [years_etalon_dict[i] for i in years_etalon_dict.keys()]
	else:
		for year in years_etalon:
			if int(years[0]) <= year and int(years[1]) >= year:
				years_for_analysis.append(years_etalon_dict[year])
	years_for_analysis = ["new" if i=="16" else i for i in years_for_analysis]

	# sources
	if sources == []:
		sources_for_analysis = [sources_etalon[i] for i in sources_etalon.keys()]
	else:
		sources_for_analysis = [sources_etalon[i] for i in sources]

	# get only required text and if print_max_min_texts print texts with max and min tones
	for text in pickle.load(open(DUMP_DIR[0]+"\\tones.dump", 'rb')):
		if ((text[0].split("\\")[-1].split("_")[0] in sources_for_analysis) and (
			text[0].split("\\")[-1].split("_")[1] in years_for_analysis)
		):
			text_for_analysis.append(text)
	if print_max_min_texts:
		text_with_max_tone = max(text_for_analysis, key = lambda i : i[1])
		text_with_min_tone = min(text_for_analysis, key = lambda i : i[1])
		print ("Text with MAX tone:\n"
			   +text_with_max_tone[0]+" "+str(text_with_max_tone[1])+"\n"
			   +open(text_with_max_tone[0], "r", encoding="utf8").read()+"\n\n")
		print ("Text with MIN tone:\n"
			   +text_with_min_tone[0]+" "+str(text_with_min_tone[1])+"\n"
			   +open(text_with_min_tone[0], "r", encoding="utf8").read()+"\n\n")
	return text_for_analysis


#ask_sentiment(True, [1997,2016], [])
