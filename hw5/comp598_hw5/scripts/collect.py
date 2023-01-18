import argparse
import requests
import json
import os
from collect_func import *

script_dir = os.path.dirname(__file__)

def main():
    posts1, posts2 = collect_posts()
    output_posts(script_dir, posts1, posts2)


if __name__ == '__main__':
    main()
