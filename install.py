#coding=utf-8




import re
from b2 import file2
from b2 import str2
import os


import_pattern = re.compile("^\s*(from|import){1}\s{1,}(test[\d\w_]{1,})\s*")
for file in file2.walk_folder("./test" , file_filter = lambda x: True if x.endswith("py") else False):
    filename = os.path.basename(file).replace("test" ,"") 
    d = dict() 
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            matcher = import_pattern.match(line)
            if matcher:
                d[matcher.group(2)] =  matcher.group(2).replace("test","")

    with open(file) as f,open("./moodstyle/%s"  % filename , "w") as w:
        for line in f:
            line = str2.replace_all( line , d) 
            w.write(line)
