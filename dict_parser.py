import re
import json

f = open("slang_dict.txt", "r")
key = ""
dic = {}

for line in f:
    
    line = line.replace("\n", "")
    line = line.replace("Meaning", "")
    line = line.replace("(online gaming)", "")
    line = line.replace("(amateur radio)", "")
    
    if line == "":
        continue
    elif key == "":
        # print(line)
        key = line
    else:
        # print(key, line)
        if key not in dic:
            dic[key] = line
        key = ""

print(dic)

with open('parsed_slang_dict.txt', 'w') as outfile:  
    json.dump(dic, outfile)