# Enter your code here. Read input from STDIN. Print output to STDOUT
import operator
import sys

PASSING = 100
NOT_STRONG = 0.01
STRONG = 1
MISSING = 0
WEIGHT = 100


char_scores = {
    'a': 8.12,
    'b': 1.49,
    'c': 2.71,
    'd': 4.32,
    'e': 12.02,
    'f': 2.30,
    'g': 2.03,
    'h': 5.92,
    'i': 7.31,
    'j': 0.10,
    'k': 0.69,
    'l': 3.98,
    'm': 2.61,
    'n': 6.95,
    'o': 7.68,
    'p': 1.82,
    'q': 0.11,
    'r': 6.02,
    's': 6.28,
    't': 9.10,
    'u': 2.88,
    'v': 1.11,
    'w': 2.09,
    'x': 0.17,
    'y': 2.11,
    'z': 0.07,
}

def get_char_weight(char):
    return char_scores[char.lower()] / WEIGHT


class CharSubstitution(object):
    def __init__(self, root):
        self.root_char = root
        self.confirmed = False
        self.chars = {}
        self.dict_score = {}
        self.maybe_score = 0.1
        self.strong_score = 1.0
        
    def is_set(self):
        return len(self.chars) != 0
    
    def is_strong(self):
        if not self.is_set():
            return False
        char = self.get_sub()
        if char not in self.chars:
            return False
        if self.chars[char] > 1:
            return True
        return False
    
    def set_to(self, other, wordlen):
        if other not in self.chars:
            self.chars[other] = 0
        self.chars[other] += 0.0001 + wordlen / 10
    
    def strongly_set_to(self, other, wordlen):
        if other not in self.chars:
            self.chars[other] = 0
        self.chars[other] += 1 + wordlen / 10
        
    def __repr__(self):
        
        sorted_chars = sorted(self.chars.items(),
                              key=operator.itemgetter(1),
                              reverse=True)
        return "%s=%s | %s" % (self.root_char, sorted_chars, self.dict_score)
    
    def get_score(self):
        if not self.is_set():
            return MISSING
        if not self.is_strong():
            return NOT_STRONG
        return STRONG
    
    def get_sub(self, rank=0):
        if not self.is_set():
            return self.root_char
        sorted_chars = sorted(self.chars.items(),
                              key=operator.itemgetter(1),
                              reverse=True)
        return sorted_chars[rank][0]
    
    def set_dict_score(self, dict_score):
        self.dict_score[self.get_sub()] = dict_score
        

def strlen(a, b):
    if len(a) > len(b):
        return 1
    return -1

known_words = []

with open('dictionary.lst', 'r') as f:
    #words = [line.strip() for line in f]
    #words = sorted(words, cmp=strlen, reverse=True)
    worddict = {}
    for line in f:
        w = line.strip()
        known_words.append(w)
        if len(w) not in worddict:
            worddict[len(w)] = []
        worddict[len(w)].append(w)
           
def decrypt(key, cipher, subs):
    if len(key) != len(cipher):
        return None, None
    char_lookups = {}
    consistent = {}
    for i in xrange(len(key)):
        if key[i] not in char_lookups:
            char_lookups[key[i]] = cipher[i]
        elif char_lookups[key[i]] != cipher[i]:
            return None, None  # not internally consistent break
        else:  # this 2nd check prevents false positives
            consistent[key[i]] = cipher[i]  # internally consistent        
    return consistent, char_lookups
    
input_str = sys.stdin.read()
input_words = sorted([w.strip() for w in input_str.split()], cmp=strlen, reverse=True)
subs = {}
for letter in range(ord('a'), ord('z')+1):
    subs[chr(letter)] = CharSubstitution(chr(letter))
for letter in range(ord('A'), ord('Z')+1):
    subs[chr(letter)] = CharSubstitution(chr(letter))
    
    
def check_score(subs, passing_grade):
    total = 0
    num_subs = len(subs)
    for key, charsub in subs.items():
        total += charsub.get_score()
    return total >= passing_grade
    
for word in input_words:
    for check in worddict[len(word)]:
        confirmed, maybes = decrypt(word, check, subs)
        if confirmed is not None:
            for key, crypt in confirmed.items():
                subs[key].strongly_set_to(crypt, len(word))
        if maybes is not None:
            for key, crypt in maybes.items():
                subs[key].set_to(crypt, len(word))
    if check_score(subs, PASSING):
        print "Reached passing score"
        break
output = ""

def get_output_score(output, wordlist):
    output_words = [w.strip() for w in output.split()]
    total_words = len(output_words)
    matches = 0
    for w in output_words:
        if w in wordlist:
            matches += 1 
    return matches / float(total_words)

for char in input_str:
    if char == ' ':
        output += ' '
        continue
    output += subs[char].get_sub()
print output
output_score = get_output_score(output, known_words)
for char, sub in subs.items():
    sub.set_dict_score(output_score)
print subs['s']

working_sub = 's'
for char in input_str:
    if char == ' ':
        output += ' '
        continue
    output += subs[char].get_sub()

print output
output_score = get_output_score(output, known_words)
subs[working_sub].set_dict_score(output_score)
