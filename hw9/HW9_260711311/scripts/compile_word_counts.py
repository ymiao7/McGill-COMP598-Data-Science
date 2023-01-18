from collections import Counter
import re
import math
import numpy as np
import argparse
import json
import pandas as pd
import os

script_dir = os.path.dirname(__file__)

def pony_id(row):
    if row['pony'].lower() == 'twilight sparkle':
        return 'twilight'
    elif row['pony'].lower() == 'applejack':
        return 'applejack'
    elif row['pony'].lower() == 'rarity':
        return 'rarity'
    elif row['pony'].lower() == 'pinkie pie':
        return 'pinkie'
    elif row['pony'].lower() == 'rainbow dash':
        return 'rainbow'
    elif row['pony'].lower() == 'fluttershy':
        return 'fluttershy'
    else:
        return 'non-Pony'

def add_column(dialog):

    new_col = dialog.apply(lambda row: pony_id(row), axis=1).values # add new col containing pony id
    dialog1 = dialog.assign(pony_id=new_col)
    pony_dialog = dialog1[dialog1['pony_id']!='non-Pony']
    pony_dialog.index = range(0,len(pony_dialog))
    return pony_dialog

def create_dict(pony_dialog):
    pony_dict = {}
    for idx, row in pony_dialog.iterrows():
        dialog_words = row.dialog
        pony = row.pony_id

        dialog_words = re.sub(r"[()\[\],-.?!:;#&]", " ", dialog_words)
        dialog_words = re.split(" ",dialog_words)
        dialog_words = list(filter(lambda a: a != '', dialog_words))
        dialog_words = [word.lower() for word in dialog_words if word.isalpha()]

        if pony not in pony_dict.keys():
            pony_dict[pony] = dialog_words
        else:
            pony_dict[pony] += dialog_words    
    return pony_dict

def create_counts(pony_dict):
    pony_count = {}
    for k, v in pony_dict.items():
        counter = Counter(v)
        pony_count[k] = {x[0]: x[1] for x in counter.most_common() if x[1] >= 5}
    return pony_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--word_counts_json', help='output file name')
    parser.add_argument('clean_dialog', help='clean_dialog.csv file')

    args = parser.parse_args()

    input_file = os.path.join(script_dir, '..', 'data', f'{args.clean_dialog}')
    out_file = args.word_counts_json

    dialog = pd.read_csv(f'{input_file}')
    pony_dialog = add_column(dialog)
    pony_dict = create_dict(pony_dialog)
    pony_count = create_counts(pony_dict)

    with open(out_file, "w") as outfile:
        json.dump(pony_count, outfile)

if __name__=='__main__':
    main()
