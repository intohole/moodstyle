#!/bin/sh


FUNCTION_FILE="README.md"



echo > ${FUNCTION_FILE}
echo "moodstyle机器学习脚本库" >> ${FUNCTION_FILE}
echo "=======================" >> ${FUNCTION_FILE}
echo "" >> ${FUNCTION_FILE}
echo "" >> ${FUNCTION_FILE}
echo "" >> ${FUNCTION_FILE}
echo "" >> ${FUNCTION_FILE}
cd `dirname $0`
CWD=`pwd`
for function_file in `ls ${CWD}/moodstyle/*.py`;do
    echo "+ `basename ${function_file}`" >> ${FUNCTION_FILE}
    cat ${function_file} | grep -En "(^class|def )" | grep -v "__" | grep -v "def _" | sed  's/class /    + /' | sed 's/def /    + /' | sed 's/:$//' | sed 's/\]/\\]/g' | sed 's/\[/\\[/g' | awk -F ":" '{
    line_number = $1;
    function_name  = ""
    for(i = 2 ;i <=NF ;i++){
        if(i != 2){
            function_name=function_name":"$i
        }else{
            function_name =$i 
        }
    }
    print function_name"](b2/'`basename ${function_file}`'#L"line_number")" 
}' | sed 's/+ /+ [/'>> ${FUNCTION_FILE} 
done
