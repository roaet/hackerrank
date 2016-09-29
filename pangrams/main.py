import string
import sys

start_string = raw_input().strip()
letters = [l for l in string.ascii_lowercase]

flags = [False for i in range(len(letters))]
for l in start_string:
    try:
        idx = letters.index(l.lower())
        flags[idx] = True
    except ValueError:
        pass

if all(flags):
    print "pangram"
else:
    print "not pangram"
