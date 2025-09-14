# Regular Expressions (REGEX)

import re

sentence = """
https://www.google.com
http://coreyms.com.ng
https://youtube.com
https://www.nasa.gov
www.test.com
"""

pattern = re.compile(r"[https]+:/{2}[a-z\.]+[a-z\.]+[a-z]")
correct_pattern = re.compile(r"https?://(www\.)?[a-zA-z]\.[a-zA-z.:]")
matches = pattern.finditer(sentence)
# print(matches)

for match in matches:
    print(match)


