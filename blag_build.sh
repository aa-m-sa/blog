#!/bin/bash

set -e

python process_tags.py

echo '...tags processed'

source ~/.rvm/scripts/rvm
rvm gemset use ghblog
jekyll build -s './blog' -d './blog/_site' --verbose

echo '...jekyll done'

cd ..
