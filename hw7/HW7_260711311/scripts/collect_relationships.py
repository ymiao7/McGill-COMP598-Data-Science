import os.path as osp
import os
import json
import argparse
import requests
from bs4 import BeautifulSoup
import hashlib

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

def extract_relationships_from_candidate_links(candidates, person_url):
    relationships = []

    for link in candidates:
        if 'href' not in link.attrs:
#             print(f'skipping {link}')
            continue

        href = link['href']
        if href.startswith('/dating') and href != person_url:
            relationships.append(href)

    return relationships


def extract_relationships(content, person_url):
    """
    Extract all the relationships in the file... which should have been downloaded 
    from whosdatingwho.com	
    """

    relationships = []
#     soup = BeautifulSoup(open(filename, 'r'), 'html.parser')
    soup = BeautifulSoup(content, 'html.parser')

    ###
    # get current relationship
    # grab the h4 with class=ff-auto-status
    status_h4 = soup.find('h4','ff-auto-status')
    
    # grab the next sibling
    key_div = status_h4.next_sibling

    # grab all the a elements
    candidate_links = key_div.find_all('a')

    relationships.extend(extract_relationships_from_candidate_links(candidate_links, person_url))
    if len(relationships) > 1:
        raise Exception('Too many relationships - should only have one')
    ###
    # get all prior relationships
    rels_h4 = soup.find('h4', 'ff-auto-relationships')
    sib = rels_h4.next_sibling

    while sib is not None and sib.name == 'p':
        candidate_links = sib.find_all('a') 
        sib = sib.next_sibling
        
        relationships.extend(extract_relationships_from_candidate_links(candidate_links, person_url))
    return relationships


def get_output(input_json):
    output_json = {}
    for ppl in input_json['target_people']:
        url = 'https://www.whosdatedwho.com/dating/'+ppl
        contents = get_url_contents(url, input_json['cache_dir'])
        relationships = extract_relationships(contents, '/dating/'+ppl)
        output_json[ppl] = [elem[8:] for elem in relationships]
    return output_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', help='input config json file')
    parser.add_argument('-o', '--output_file', help='output file name')

    args = parser.parse_args()

    input_fname = args.config_file
    output_fname = args.output_file

    with open(input_fname, 'r') as infile:
        input_json = json.load(infile)

    output_json = get_output(input_json)

    with open(output_fname, "w") as outfile:
        json.dump(output_json, outfile)


if __name__ == '__main__':
    main()
