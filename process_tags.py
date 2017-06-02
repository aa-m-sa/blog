#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import re

markdown = ['md', 'markdown']

unsorted_re = re.compile(r'^\[([a-zA-Z_.0-9]+, )*([a-zA-Z_.0-9]*)\]$')

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

def main_unsorted():
    for post in get_md_posts():
        with open(post, 'r') as f:
            cts_lines = f.readlines()
        if not '<!--unsorted-->' in [''.join(l.strip()) for l in cts_lines]:
            continue
        if '<!--unsorted_processed-->' in [''.join(l.strip()) for l in cts_lines]:
            continue

        # else
        cur = ''
        prev = ''
        categories = ['unsorted_links']
        tags = []
        for l in cts_lines:
            prev = cur
            cur = l.strip()
            m =unsorted_re.match(cur)
            if not (('###' in prev) and m):
                continue
            cur_wob = cur.strip('[]')
            pieces = cur_wob.split(',')
            for p in pieces:
                ps = p.split('.')
                if len(ps) > 0:
                    # lone category
                    categories.append(ps[0].strip())
                if len(ps) == 2:
                    # category.tag
                    tags.append(p.strip())
        block_limit = None
        cts_lines_filt = []
        for i, l in enumerate(cts_lines):
            if l.strip() == '---' and i > 0:
                block_limit = i
            if ('categories:' in l) and block_limit is None:
                cts_lines_filt.append('\n')
                continue
            if ('tags:' in l) and block_limit is None:
                cts_lines_filt.append('\n')
                continue
            cts_lines_filt.append(l)

        cats_text = 'categories: ['+ ', '.join(categories) + ']\n'
        tags_text = 'tags: ['+ ', '.join(tags) + ']\n'
        cts_lines_filt.insert(block_limit+1, '<!--unsorted_processed-->\n')
        cts_lines_filt.insert(block_limit-1, cats_text)
        cts_lines_filt.insert(block_limit, tags_text)


        with open(post, 'w') as f:
            f.writelines(cts_lines_filt)



def main_tags():
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

if __name__ == "__main__":
    main_unsorted()
    main_tags()


