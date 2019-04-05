#!/bin/bash

function check() {
  if [ $? != 0 ]
  then
    abort "$1 failed."
  fi
}

function abort() {
  echo -e "\033[33m$1\033[0m"
  echo -e "\033[31;1mTAGGING FAILED\033[0m"
  exit 1
}

function info() {
  echo -e "\033[34m$1\033[0m"
}

# check if everything is committed
CLEAN=`git status -s`
if [ ! -z "$CLEAN" ]
then
   abort "Working directory not clean. Please commit all changes before tagging."
fi

info "Fetching origin..."
git fetch origin > /dev/null

# get current branch
BRANCH=`git branch | grep "^*" | cut -d " " -f 2`
info "Current branch is $BRANCH."

# check if local branch is origin branch
LOCAL_COMMIT=`git show --format="%H" $BRANCH`
ORIGIN_COMMIT=`git show --format="%H" origin/$BRANCH`

if [ "$LOCAL_COMMIT" != "$ORIGIN_COMMIT" ]
then
   abort "Local $BRANCH is not up to date."
fi

pytest -vs --cache-clear
check "pytest"

python setup.py sdist bdist_wheel
twine check dist/*.whl
check "packaging"

# get the version
VERSION=`python setup.py --version`
info "Current version $VERSION"

# check if tag to create has already been created
EXISTS=`git tag | grep $VERSION`
if [ "$VERSION" == "$EXISTS" ]
then
   abort "Revision $VERSION already tagged."
fi

# check if VERSION is in head of CHANGES.rst
REV_NOTE=`grep "$VERSION" CHANGES.rst`
if [ -z "$REV_NOTE" ]
then
    abort "No notes for revision $VERSION found in CHANGES.rst"
fi

info "Creating tag $VERSION..."
git tag -a "$VERSION" -m "Tag release for revision $VERSION"
git push --tags
info "Done."
