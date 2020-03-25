from nltk.corpus import wordnet
import re
import itertools
 

import json, math
from pprint import pprint as pp

def whatisthis(testword):
    """Return a list

    This function is responsible for querying the wordnet database and returning a list of what the word could be.
    Get the hypernyms (catagory) of the word and strip wordnet syntax.
    Fall back on canonical form, dictionary form, or citation form if there is no higher catagory.
    Filter the list of redundent elements.
    """
    whats = list()
    pattern = re.compile('([^\s\w]|_)+')

    testword = pattern.sub('', testword)
    syns = wordnet.synsets(testword)

    for syn in syns:
        whats.append(str(syn.hypernyms())[9:].split(".", 1)[0].lower())

    if not whats:
        for syn in syns:
            for lemma in synset.lemmas():
                whats.append(lemma.name().lower())

    def thefilter(word,testword):
        ls = [testword, "", None, " "]
        if word in ls:
            return False
        else: 
            return True

    whats = list(filter(lambda what: thefilter(what, testword), list(dict.fromkeys(whats))))
    return whats

def doubleword_label_handeling(testword):
    whats = []
    testwords = testword.split(" ")

    for word in testwords:
        out = whatisthis(word)
        whats = whats + out
    
    return whats

def convert_to_wordnet(words):
    wordnet = lambda word: doubleword_label_handeling(word)
    cwords = list(map(wordnet, words))

    return cwords

# True: advertisement 
def wordnet_check(images, words):
    cimages = convert_to_wordnet(images)
    cwords = convert_to_wordnet(words)

    #Flatten lists 
    cimages = list(itertools.chain(*cimages))
    cwords = list(itertools.chain(*cwords))

    cimages.extend(images)
    cwords.extend(words)

    pp(cimages)
    pp(cwords)

    outcomes = []
    for image in cimages:
        if image in cwords:
            outcomes.append(True)
        else:
            outcomes.append(False)

    if outcomes.count(False) == 0:
        return False
    else:
        return True

def compare(data):
    images = data["image"]
    contents = data["content"]

    words = [ v for v in contents["word"].values() ]
    print(wordnet_check(images, words))

    return "sdfhhjk"

def testing_compare(fname="inputcompare.json"):
    with open(fname) as json_file:
        data = json.load(json_file)

    compare(data)

    
def calculateDistance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist 

def calculateScore(data, word):
    contents = data["content"]
    score = 0

    for index in contents["word"]:
        val = calculateDistance(word["x"], word["y"], contents["x1"][index], contents["x2"][index])

        print(index, val)
        print(word["x"], word["y"], contents["x1"][index], contents["x2"][index])

        score += val
        print(score)
    
    return score

def distance_metrics(data, word):
    images = data["image"]
    contents = data["content"]

    


def testing_dist(fname="inputcompare.json"):
    with open(fname) as json_file:
        data = json.load(json_file)

    calculateScore(data, {"guess":"looming","x":1.170817852,"y":-0.2876406908})
    
if __name__ == "__main__":
    #red-breasted merganser, red wine
    print(doubleword_label_handeling("red wine"))
    print(calculateDistance(4, 0, 4, 8))
    testing_dist()
