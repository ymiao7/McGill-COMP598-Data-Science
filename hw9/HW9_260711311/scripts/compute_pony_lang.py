from collections import Counter
import re
import math
import numpy as np
import argparse
import json
import pandas as pd
import os

script_dir = os.path.dirname(__file__)

def create_tfidf(input_json):
    pony_tfidf = {}

    N = 0
    word_freq = {}
    for pony, words in input_json.items():
        temp_N = sum([v for k, v in words.items()])
        N += temp_N
    
        for word, count in words.items():
            if word not in word_freq.keys():
                word_freq[word] = input_json[pony][word]
            else:
                word_freq[word] += input_json[pony][word]


    for pony, words in input_json.items():
        pony_tfidf[pony] = {}
        for word, freq in words.items():
            tf = input_json[pony][word]
            idf = math.log(N / word_freq[word])
            pony_tfidf[pony][word] = tf*idf

    return pony_tfidf


def create_tfidf1(input_json):
    pony_tfidf = {}

    N = 0
    for pony, words in input_json.items():
        temp_N = sum([v for k, v in words.items()])
        N += temp_N

    for pony, words in input_json.items():
        pony_tfidf[pony] = {}
        for word, freq in words.items():

            tf = input_json[pony][word]
            N_ponies = len(input_json)
            df = 0
            for k, v in input_json.items():
                if word in v.keys():
                    df+=1
            idf = math.log(N_ponies/df)

            pony_tfidf[pony][word] = tf*idf

    return pony_tfidf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true')
    parser.add_argument('input_file',help='pony_counts.json')
    parser.add_argument('num_words', help='number of top ranked terms for each pony')


    args = parser.parse_args()
    input_fname = os.path.join(script_dir, '..', 'data', f'{args.input_file}')
    num_words = int(args.num_words)

    with open(input_fname, 'r') as infile:
        input_json = json.load(infile)

    if args.p:
        pony_tfidf = create_tfidf1(input_json)
    else:
        pony_tfidf = create_tfidf(input_json) 

    stdout = {k:[k1 for k1, v1 in sorted(v.items(), key=lambda item: item[1],reverse=True)[:num_words]] for k, v in pony_tfidf.items()}
    print(json.dumps(stdout, indent=4))

if __name__=='__main__':
    main()
