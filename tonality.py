from __future__ import print_function
from alchemyapi import AlchemyAPI
import os
import glob
import codecs
import string
import re
import pymorphy2
import pickle
import collections
from operator import itemgetter
import json

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

dir_path = 'data/*/*.txt'
all_texts = glob.glob(dir_path)

for text in all_texts:
response = alchemyapi.entities('text', text, {'sentiment': 1})

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Entities ##')
    for entity in response['entities']:
        print('text: ', entity['text'].encode('utf-8'))
        print('type: ', entity['type'])
        print('relevance: ', entity['relevance'])
        print('sentiment: ', entity['sentiment']['type'])
        if 'score' in entity['sentiment']:
            print('sentiment score: ' + entity['sentiment']['score'])
        print('')
else:
    print('Error in entity extraction call: ', response['statusInfo'])

response = alchemyapi.keywords('text', text, {'sentiment': 1})

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Keywords ##')
    for keyword in response['keywords']:
        print('text: ', keyword['text'].encode('utf-8'))
        print('relevance: ', keyword['relevance'])
        print('sentiment: ', keyword['sentiment']['type'])
        if 'score' in keyword['sentiment']:
            print('sentiment score: ' + keyword['sentiment']['score'])
        print('')
else:
    print('Error in keyword extaction call: ', response['statusInfo'])

response = alchemyapi.concepts('text', text)

if response['status'] == 'OK':
    print('## Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Concepts ##')
    for concept in response['concepts']:
        print('text: ', concept['text'])
        print('relevance: ', concept['relevance'])
        print('')
else:
    print('Error in concept tagging call: ', response['statusInfo'])

response = alchemyapi.language('text', text)

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Language ##')
    print('language: ', response['language'])
    print('iso-639-1: ', response['iso-639-1'])
    print('native speakers: ', response['native-speakers'])
    print('')
else:
    print('Error in language detection call: ', response['statusInfo'])

response = alchemyapi.sentiment_targeted('text', text, 'Denver')

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))
    maximum = 0
    minimum = 0
    if maximum < response:
        maximum = response
        name_positive_text = text
    else:
        minimum = response
        name_negative_text = text

    print('')
    print('## Targeted Sentiment ##')
    print('type: ', response['docSentiment']['type'])
    print('positive text is ', name_positive_text)
    print('negative text is ', name_negative_text)

    if 'score' in response['docSentiment']:
        print('score: ', response['docSentiment']['score'])
else:
    print('Error in targeted sentiment analysis call: ',
          response['statusInfo'])