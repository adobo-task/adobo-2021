import sys
import json
import spacy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--add-offset", action="store_true")
parser.add_argument("--use-space-as-col-sep", action="store_true")
args = parser.parse_args()

nlp = spacy.load("es_core_news_sm")

sep = ' ' if args.use_space_as_col_sep else '\t'

with open('/dev/stdin') as f:
    for line in f:
        data = json.loads(line)
        data['text'] = data['text'].replace(u'\xa0', u' ')
        sentence = []
        doc = nlp(data['text'])
        labels = [label for label in data['labels']]
        labels.sort(key=lambda x: x[1])
        i = 0
        j = 0
        while i < len(doc) and j < len(labels):
            if doc[i].idx == labels[j][0]:
                pref = 'B-'
                while i < len(doc) and doc[i].idx < labels[j][1]:
                    print(f'{doc[i].text}{sep}{pref + labels[j][2]}', end='')
                    print(f'{sep}{doc[i].idx}' if args.add_offset else '')
                    i += 1
                    pref = 'I-'
                j += 1
                pass
            else:
                if doc[i].text != ' ':
                    print(f'{doc[i].text}{sep}O', end='')
                    print(f'{sep}{doc[i].idx}' if args.add_offset else '')
                i += 1
        assert(j >= len(labels))
        while i < len(doc):
            if doc[i].text != ' ':
                print(f'{doc[i].text}{sep}O', end='')
                print(f'{sep}{doc[i].idx}' if args.add_offset else '')
            i += 1
        print()


