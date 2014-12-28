#!/bin/bash
if [ ! -d venv ] ; then
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

if [ ! /var/www/lancealbertson.com/htdocs ] ; then
  ln -sf /var/www/lancealbertson.com/htdocs output
fi

source venv/bin/activate
git pull --quiet
git submodule update --quiet --init
make clean
make html
deactivate
