from nltk.corpus import wordnet
import re

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


def compare(image, content):
    print(image, content)
    return "sdfhhjk"

if __name__ == "__main__":
    #red-breasted merganser, red wine
    print(whatisthis("hen-of-the-woods"))
    print(doubleword_label_handeling("red wine"))