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
            for lemma in syn.lemmas():
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
def wordnet_check_quick(images, words):
    cimages = convert_to_wordnet(images)
    cwords = convert_to_wordnet(words)

    #Flatten lists 
    cimages = list(itertools.chain(*cimages))
    cwords = list(itertools.chain(*cwords))

    cimages.extend(images)
    cwords.extend(words)

    outcomes = []
    for image in cimages:
        if image in cwords:
            outcomes.append(True)
        else:
            outcomes.append(False)

    if outcomes.count(True) == 0:
        return "Theres advertisement(s)"
    else:
        return True

def compare(data):
    images = data["image"]
    contents = data["content"]

    words = [ v for v in contents["word"].values() ]
    out = wordnet_check_quick(images, words)

    return out


#score calculator  
def calculateDistance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist 

def calculateScores(data):
    contents = data["content"]
    scores = {}

    for index in contents["word"]:
        score = 0
        for j in contents["word"]:
            val = calculateDistance(contents["x"][index], contents["y"][index], contents["x"][j], contents["y"][j])
            score += val

        scores[contents["word"][index]] = score

    
    print(scores)
    return scores

#match words
def lookup(images, words):
    words = list(words)
    words = words + images
    lookup = {}
    for word in words:
        whats = doubleword_label_handeling(word)
        lookup[word] = whats

    return lookup

def get_ads(lookup, scores, data):
    #get ads
    ads = []
    for image in data["image"]:
        whatsi = lookup[image]
        print(whatsi)
        for score in scores:
            whatss = lookup[score]
            x = filter(lambda item: any(x in item for x in whatsi), whatss)

            for i in x:
                if type(i) == str:
                    ads.append(score)
    print(ads)
    ads = list(dict.fromkeys(ads))

    print("below:-----------------------------------")
    print(ads)
    print(data["image"])

    return ads


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def Likely(scores, ads):
    text = ""
    vscores = list(scores.values())
    minim = min(vscores)
    maxim = max(vscores)
    ranges = chunkIt(range(int(round(minim)), int(round(maxim))),3)

    for ad in ads:
        sc = int(round(scores[ad]))
        if sc in ranges[0]:
            text = text + ad + ": most likely not an advertisement\n"

        if sc in ranges[1]:
            text = text + ad + ": very likely not an advertisement\n"

        if sc in ranges[2]:
            text = text + ad + ": likely not an advertisement\n"

        if sc > ranges[2][-1]:
            text = text + ad + ": possibly not an advertisement\n"
            
    return text

def advert(data):
    #remove double words
    imagels = data["image"]
    outls = []

    for i in imagels:
        ls = i.split(" ")
        outls = outls + ls

    data["image"] = outls

    adbool = compare(data)
    if isinstance(adbool, str) :
        return adbool
    else:
        scores = calculateScores(data)
        lookupt = lookup(data["image"], data["content"]["word"].values())
        ads = get_ads(lookupt, scores, data)
        return Likely(scores, ads)


def testing_dist(fname="inputcompare.json"):
    with open(fname) as json_file:
        data = json.load(json_file)
    """
    scores = calculateScores(data)
    lookupt = lookup(data["image"], data["content"]["word"].values())
    ads = get_ads(lookupt, scores, data)
    print(Likely(scores, ads))
    """
    print(advert(data))

def testing_compare(fname="inputcompare.json"):
    with open(fname) as json_file:
        data = json.load(json_file)

    compare(data)
   
if __name__ == "__main__":
    print(doubleword_label_handeling("car wheel"))
    testing_dist()
    testing_compare()
