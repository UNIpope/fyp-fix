from nltk.corpus import wordnet
synset = wordnet.synsets("jersey")
print(synset)

print(synset[0].name())
print(synset[0].lemmas()[0].name())
print(synset[0].definition())
print(str(synset[0].examples()))
print("---------------------------------------------------------------")
syn = list()
ant = list()
for synset in wordnet.synsets("jersey"):
    for lemma in synset.lemmas():
        syn.append(lemma.name())    #add the synonyms
        #if lemma.antonyms():    #When antonyms are available, add them into the list
            #ant.append(lemma.antonyms()[0].name()

print("Synonyms: " + str(syn))
##print('Antonyms: ' + str(ant))

print("---------------------------------------------------------------")
set_ = wordnet.synset('jersey.n.03')
print(set_.hypernyms())
print(set_.hyponyms())
print(set_.member_holonyms())
print(set_.root_hypernyms())
print("---------------------------------------------------------------")

"""
from nltk.corpus import wordnet
from pprint import pprint
syn = list()
for synset in wordnet.synsets("jersey"):
    for lemma in synset.lemmas():
        syn.append(lemma.name())

pprint("Synonyms: " + str(syn))

"""

from nltk.corpus import wordnet

sy = wordnet.synsets("jersey")
for nn in sy:
    print(nn.hypernyms())

