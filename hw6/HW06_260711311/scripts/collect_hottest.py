import argparse
import requests
import json
import os

script_dir = os.path.dirname(__file__)

def collect_posts(subreddit):
    posts = []
    post_id = None

    for i in range(5):
        data = requests.get(f'http://api.reddit.com{subreddit}/hot?limit=100&after={post_id}'
                            ,headers={'User-Agent': 'macos:requests (by /u/ymiao7)'})

        content = [elem for elem in data.json()['data']['children']]

        post_id = data.json()['data']['after']
        posts += content
        
    return posts[:500]

def output_posts(script_dir, posts, json_name):
    with open(os.path.join(script_dir, '..','data',json_name), "w") as outfile:
        for post in posts:
            json.dump(post, outfile)
            outfile.write('\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output_file',help='the name of the output json file')
    parser.add_argument('subreddit')

    args = parser.parse_args()
    json_name = args.output_file

    posts = collect_posts(args.subreddit)

    output_posts(script_dir, posts, json_name)

if __name__=='__main__':
    main()
