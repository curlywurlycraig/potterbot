from __future__ import print_function

import glob
import random
import math

from nltk.tokenize import word_tokenize
from collections import Counter, defaultdict

filenames = glob.glob("*.srt")

language_model = defaultdict(Counter)

print("welcome to the harry potter character emulator")

print("training language model")
for filename in filenames:
    with open(filename) as f:
        print("Reading lines from {}...".format(filename))

        # all lines not beginning with a number are dialog lines
        for line in f:
            if line[0] not in "0123456789":
                words = word_tokenize(line)
                if len(words) == 0:
                    continue

                language_model['0start'][words[0]] += 1
                for i, word in enumerate(words):
                    if i < len(words) - 2:
                        next_word = words[i+1]
                        language_model[word][next_word] += 1
                    else:
                        language_model['1end'][words[i]] += 1

def generate_sentence():
    result = ""
    next_word = '0start'

    while next_word is not '.' and next_word is not '1end':
        if next_word is not '0start':
            result += next_word + " "

        most_common = language_model[next_word].most_common()
        if len(most_common) == 0:
            return result

        total_occurrences = sum([count[1] for count in most_common])
        random_number = random.random() * math.floor(total_occurrences)

        for word, count in most_common:
            if random_number <= count:
                next_word = word
                break
            else:
                random_number -= count

    result += "."
    return result

# generate 10 sentences
print()
for i in range(10):
    print("Potterbot: {}".format(generate_sentence()))

