import argparse
import requests
import json
import os
from compute_title_lengths_func import *

script_dir = os.path.dirname(__file__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',help='the input json file')

    args = parser.parse_args()
    input_file = os.path.join(script_dir, '..', 'data', f'{args.input_file}')

    sample = read_in(input_file)
    print('Average post title length for sample is:',"{:.2f}".format(compute_avg_len(sample)))



if __name__ == '__main__':
    main()
