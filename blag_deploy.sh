#!/usr/bin/env bash

# assumes env variable BLAG_DEPLOY_TGT

rsync -avz blog/_site/ $BLAG_DEPLOY_TGT

# ...YEAAAH.
