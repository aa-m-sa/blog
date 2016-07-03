#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml

markdown = ['md', 'markdown']

posts_dir = 'blog/_posts/'
active_tags_f = 'blog/_data/tags.yml'
all_tags_f = 'blog/_data/tags_all.yml'

def get_md_posts(posts_dir=posts_dir):
    #
    for path, dir, files in os.walk(posts_dir):
        for f in files:
            if f.split('.')[-1] in markdown:
                yield os.path.join(path,f)

def add_tags(tags_from, tags_to):
    for k in tags_from:
        if k not in tags_to:
            tags_to[k] = []
        for t in tags_from[k]:
            if t not in tags_to[k]:
                tags_to[k].append(t)
    return tags_to

tags = dict()

for post in get_md_posts():
    with open(post, 'r') as f:
        cts = f.read()
        y = yaml.load(cts.split('---')[1])
        if not 'tags' in y:
            continue
        for t in y['tags']:
            try:
                a, b  = t.split('.')
            except ValueError:
                a = 'uncateg'
            if not a in tags:
                tags[a] = []
            if not t in tags[a]:
                tags[a].append(t)


with open(active_tags_f, 'r') as f:
    active_tags_old = yaml.load(f)

with open(active_tags_f, 'w') as f:
    f.write(yaml.dump(tags))

with open(all_tags_f, 'r') as f:
    all_tags_old = yaml.load(f)

all_tags = add_tags(active_tags_old, all_tags_old)
all_tags = add_tags(tags, all_tags_old)

with open(all_tags_f, 'w') as f:
    f.write(yaml.dump(all_tags))



