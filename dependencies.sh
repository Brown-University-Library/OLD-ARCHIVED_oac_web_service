#!/bin/bash

mkdir tmp-pip
pip install -r requirements.txt -t tmp-pip
cd tmp-pip
rm -f site-packages.zip
zip -r site-packages.zip *
mv -f site-packages.zip ../WEB-INF/lib-python/site-packages.zip

# zip -r -9 jython-lib.zip /home/dev/.pythonz/pythons/Jython-2.5.2/Lib/*
# mv -f jython-lib.zip ../WEB-INF/lib-python/jython-lib.zip