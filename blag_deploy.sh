#!/usr/bin/env bash

git checkout deploy

set -e

# build and deploy

./blag_build.sh

# assumes env variable BLAG_DEPLOY_TGT

if [ -z "$BLAG_DEPLOY_TGT"]
then
    echo "needs target"
    exit 1
fi

echo $BLAG_DEPLOY_TGT
rsync -avz blog/_site/ $BLAG_DEPLOY_TGT

# ...YEAAAH.
