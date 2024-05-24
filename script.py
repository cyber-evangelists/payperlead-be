import re

string = ""

print(re.search("@(.*),(.*),", string).group(2))
