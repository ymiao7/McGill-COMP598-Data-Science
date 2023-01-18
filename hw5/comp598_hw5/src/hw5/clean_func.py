import json
import argparse
import datetime


def is_json(myjson):
    """
    check if each line is a valid json dictionary
    """

    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def read_in(file_name):
    """
    read in the posts
    returns a list of posts
    """

    with open(file_name,'r') as f:
        content = f.readlines()

    posts = []
    for line in content:
        if is_json(line):
            posts.append(json.loads(line))
    return posts

def rename_title(p):
    """
    rename "title_text" to "title"
    returns a list of posts with renamed titles
    """
    for post in p:
        for k, v in post.items():
            if k=='title_text':
                post['title']=post['title_text']
                del post['title_text']
    return p

def datetime_valid(p):
    """
    check if the "createdAt" datetime is valid for each post
    """

    if "createdAt" in p:
        time = p["createdAt"]
        #########
        try:
            datetime.datetime.strptime(time[:-3]+time[-2:],'%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            try:
                datetime.datetime.strptime(time,'%Y-%m-%dT%H:%M:%S%z')

            except:
                return False
        except:
            return False

        #########

    else:
        return True

    return True

def create_output(output,p):
    """
    create output json file
    """

    with open(output, "w") as outfile:
        for post in p:
            json.dump(post, outfile)
            outfile.write('\n')

def to_utc(p):
    for post in p:
        time = post["createdAt"]
        try:
            post["createdAt"] = datetime.datetime.strptime(time[:-3]+time[-2:],'%Y-%m-%dT%H:%M:%S%z').astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")

        except:
            post["createdAt"] = datetime.datetime.strptime(time,'%Y-%m-%dT%H:%M:%S%z').astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    return p


