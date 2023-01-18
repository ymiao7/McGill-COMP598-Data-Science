import requests
from bs4 import BeautifulSoup
import hashlib
import os.path as osp
import os
import json
import re
import pandas as pd
import argparse


def get_url_contents(url, cache_dir, use_cache=True):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    fname = hashlib.sha1(url.encode('utf-8')).hexdigest()
    full_fname = osp.join(cache_dir, fname)
    contents = None
    if osp.exists(full_fname) and use_cache == True:
        print('Loading from cache')
        contents = open(full_fname, 'r').read()
    else:
        print('Loading from source')
        r = requests.get(url)
        contents = r.text
        with open(full_fname, 'w') as fh:
            fh.write(contents)
    return contents

def extract_course_info(cache_dir, page_num):    

    url = f'https://www.mcgill.ca/study/2020-2021/courses/search?page={page_num}'
    contents = get_url_contents(url, cache_dir)

    soup = BeautifulSoup(contents, 'html.parser')
    status_h4 = soup.find('h4','field-content')
    candidates = status_h4.parent.parent.parent.find_all('a')

    course_info = {}

    for link in candidates:
        #print(link)
        tmp = re.search(r'(\w+\s\w+)(.*)\((.*) credit[s]?\)', link.string.replace('\n',''))
        #course = [tmp.group(1), tmp.group(2).strip(), tmp.group(3)]
        try:
            courseid = tmp.group(1)
            course_name = tmp.group(2).strip()
            credits = tmp.group(3)
        except:
            continue
	
    

        info = [courseid, course_name, credits]
        for idx, col in enumerate(['CourseID', 'Course Name', '# of credits']):
            if col not in course_info:
                course_info[col] = [info[idx]]
            else:
                course_info[col] += [info[idx]]
    

    return course_info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--caching_dir',help='cache directory')
    parser.add_argument('page_num')

    args = parser.parse_args()

    course_info = extract_course_info(args.caching_dir, args.page_num)

    df = pd.DataFrame(course_info)
    print(df.to_csv(index=False)[:-1])



if __name__=='__main__':
    main()
