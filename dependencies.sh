#!/bin/bash
mkdir tmp-pip
pip install -r requirements.txt -t tmp-pip
zip -r WEB-INF/lib-python/site-packages.zip tmp-pip/*
rm -rf tmp-pip
