#!/bin/sh


CWD=$(cd `dirname $0` ; pwd)
INSTALL_PATH=${CWD}/moodstyle
for i in `ls test/*`;do
    new_name=`basename $i | sed 's/^test//g'`
    cp ${i} ${INSTALL_PATH}/${new_name}
done
for i in `ls ${INSTALL_PATH}/*.py`;do 
    sed -i 's/^import test/import /g' ${i} 
    sed -i 's/^from test/from /g' ${i}
done 

