#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tweets about a blog post '''

# rude and ugly

# assume the jekyll post permalink format is <markdown filename /wo date>.html

import sys
import json
import twitter
import requests


config_path = "./blag_tweet_config.json"

def load_config():
    with open(config_path, 'r') as cf:
        config = json.load(cf)
    return config

def get_title_html(md_file_path):

    md_file = md_file_path.replace('blog/_posts/', '')

    title_html = md_file[11:].replace('.md', '.html')

    print title_html

    return title_html


def main():

    try:
        config = load_config()
    except:
        print "could not load config"
        sys.exit(2)

    api = twitter.Api(consumer_key=config["consumer_key"],
                      consumer_secret=config["consumer_secret"],
                      access_token_key=config["access_token"],
                      access_token_secret=config["access_secret"])

    md_file = sys.argv[1]

    title_html = get_title_html(md_file)

    url = "%s%s" % (config["basepath"], title_html)

    # check that url works:
    try:
        r = requests.get(url)
        if not r.status_code == 200:
            raise ValueError("status not 200")
    except:
        print "error: problem with request %s" % url
        sys.exit(2)

    message = "%s %s" % (config["preamble"], url)
    print "message len %s" % len(message)

    try:
        print message
        status = api.PostTweet(message)
    except:
        print "error: problem with PostTweet"
        sys.exit(2)

if __name__ == "__main__":
    main()
