import json
import argparse
import datetime
from clean_func import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file',help='the input json file')
    parser.add_argument('-o','--output_file',help='the name of the output json file')
    args = parser.parse_args()

    input_file = args.input_file
    json_name = args.output_file

    posts = read_in(input_file)
    posts_rename_title = rename_title(posts)
    posts_datetime_valid = [post for post in posts_rename_title if datetime_valid(post)]

    # convert valid datetime in each post to utc
    posts_utc = to_utc(posts_datetime_valid)

    # keep only the posts with "title" field
    posts_with_title = [post for post in posts_utc if 'title' in post]

    # output the cleaned json
    create_output(json_name, posts_with_title)

if __name__=='__main__':
    main()
