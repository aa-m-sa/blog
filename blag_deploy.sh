#!/usr/bin/env bash

git checkout deploy

# build and deploy

./blag_build.sh

# assumes env variable BLAG_DEPLOY_TGT

rsync -avz blog/_site/ $BLAG_DEPLOY_TGT

# ...YEAAAH.
