#!/bin/sh


CWD=$(cd `dirname $0` ; pwd)
cp ${CWD}/test/*.py ${CWD}/moodstyle/cool/
python ${CWD}/setup.py install 
