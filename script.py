import re

string = "https://www.google.com/maps/place/LRF+Heating+%26+Building+Ltd/@51.7615896,-2.3128954,15z/data=!4m2!3m1!1s0x0:0x60e5a41015b7245?sa=X"

print(re.search("@(.*),(.*),", string).group(2))
