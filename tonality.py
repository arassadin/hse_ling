from __future__ import print_function
from alchemyapi import AlchemyAPI
import glob
import json

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

dir_path = 'data/*/*.txt'
all_texts = glob.glob(dir_path)


def sentiment(path):
    maximum = 0
    minimum = 0
    text_tolality = []

    path_files = path + '/*/*.txt'
    texts = glob.glob(path_files)
    for text in texts:
        with open(text, 'r') as myfile:
            file = myfile.read().replace('\n', '')
        response = alchemyapi.sentiment_targeted('text', file, 'Denver')
        if response['status']=='OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))
            for i in range(texts):
                text_tolality.append(text)
                for j in range(texts):
                    text_tolality[i].append(response)
            text_tolality.sort(response)
            f = open('text.txt', 'w')
            f.write(text_tolality)
            f.close()
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
    return text_tolality
