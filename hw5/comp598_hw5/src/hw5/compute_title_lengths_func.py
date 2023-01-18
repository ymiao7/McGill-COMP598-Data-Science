import argparse
import requests
import json


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


def compute_avg_len(p):
    """
    computes and returns the average post title length
    """
    return sum([len(p[i]['data']['title']) for i in range(len(p))])/len(p)
