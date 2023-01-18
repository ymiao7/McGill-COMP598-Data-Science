import pandas as pd
import requests
import os
import argparse
import json
from random import sample

def read_in(file_name):
    """
    read in the posts
    returns a list of posts
    """

    with open(file_name,'r') as f:
        content = f.readlines()

    posts = []
    for line in content:
        posts.append(json.loads(line))
    return posts


def sample_posts(posts,num_posts_to_output):
    names = [posts[idx]['data']['name'] for idx in range(len(posts))]
    
    if num_posts_to_output <= len(posts):
        names_sampled = sample(names,num_posts_to_output)
    else:
        names_sampled = names

    posts_sampled = {}
    for post in posts:
        if post['data']['name'] in names_sampled:
            posts_sampled[post['data']['name']] = post['data']['title']

    return posts_sampled


def output_to_tsv(out_file, posts_sampled):
    with open(out_file, "w") as f:
        print("%s\t%s\t%s" % ('Name','title','coding'), file=f)
        for k,v in posts_sampled.items():
            print("%s\t%s\t%s" % (k,v,''), file=f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_file', help='output file name')
    parser.add_argument('json_file', help='Reddit_json')
    parser.add_argument('num_posts_to_output',help='outputs a random selection of posts')

    args = parser.parse_args()

    json_file = args.json_file
    out_file = args.output_file
    num_posts_to_output = args.num_posts_to_output

    posts = read_in(json_file)

    posts_sampled = sample_posts(posts, int(num_posts_to_output))
    output_to_tsv(out_file, posts_sampled)

if __name__=='__main__':
    main()
