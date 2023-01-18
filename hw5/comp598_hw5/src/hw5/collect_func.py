import argparse
import requests
import json
import os


def collect_posts():
    num_posts = 100
    posts1 = []
    posts2 = []
    sample1 = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
    sample2 = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']
    for posts,subreddit in [(posts1, sample1), (posts2, sample2)]:
        for name in subreddit:
            data = requests.get(f'http://api.reddit.com/r/{name}/new?limit={num_posts}',
                headers={'User-Agent': 'macos:requests (by /u/ymiao7)'})


            content = [elem for elem in data.json()['data']['children']]
            posts += content
    
    return posts1, posts2



def output_posts(script_dir, posts1, posts2):
    for json_name, posts in [("sample1.json",posts1),("sample2.json",posts2)]:
        with open(os.path.join(script_dir, '..','data',json_name), "w") as outfile:
            for post in posts:
                json.dump(post, outfile)
                outfile.write('\n')
