import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

import multiprocessing
from numba import cuda
# import tensorflow as tf 
# AttributeError: 'module' object has no attribute 'placeholder'
# use api 1 as is removed in 2
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


"""
aneesh joshi (2017) Learn Word2Vec by implementing it in tensorflow (tutorial)
https://towardsdatascience.com/learn-word2vec-by-implementing-it-in-tensorflow-45641adaf2ac

"""
def matchvword(vectors, words): 
    df = pd.DataFrame(vectors, columns = ['x', 'y'])
    df['word'] = words
    df = df[['word', 'x', 'y']]

    return df.to_json()

    
def train_data(train_op, X_train, Y_train, loss, W1, b1, x, y_label):
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    iteration = 12000
    for i in range(iteration):
        # input is X_train which is one hot encoded word
        # label is Y_train which is one hot encoded neighbor word
        sess.run(train_op, feed_dict={x: X_train, y_label: Y_train})
        
        if i % 3000 == 0:
            #print('iteration '+str(i)+' loss is : ', sess.run(loss, feed_dict={x: X_train, y_label: Y_train}))
            sess.run(loss, feed_dict={x: X_train, y_label: Y_train})
    # Now the hidden layer (W1 + b1) is actually the word look up table
    vectors = sess.run(W1 + b1)

    return vectors


# function to convert numbers to one hot vectors
def to_one_hot_encoding(index, ONE_HOT_DIM):
    one_hot_encoding = np.zeros(ONE_HOT_DIM)
    one_hot_encoding[index] = 1
    return one_hot_encoding


def computational_graph(words, word2int, data, df):
    ONE_HOT_DIM = len(words)
    X = [] # input word
    Y = [] # target word

    for x, y in zip(df['input'], df['label']):
        X.append(to_one_hot_encoding(word2int[x], ONE_HOT_DIM))
        Y.append(to_one_hot_encoding(word2int[y], ONE_HOT_DIM))

    # convert them to numpy arrays
    X_train = np.asarray(X)
    Y_train = np.asarray(Y)

    # making placeholders for X_train and Y_train
    x = tf.placeholder(tf.float32, shape=(None, ONE_HOT_DIM))
    y_label = tf.placeholder(tf.float32, shape=(None, ONE_HOT_DIM))

    # word embedding will be 2 dimension for 2d visualization
    EMBEDDING_DIM = 2 

    # hidden layer: which represents word vector eventually
    W1 = tf.Variable(tf.random_normal([ONE_HOT_DIM, EMBEDDING_DIM]))
    b1 = tf.Variable(tf.random_normal([1])) #bias
    hidden_layer = tf.add(tf.matmul(x,W1), b1)

    # output layer
    W2 = tf.Variable(tf.random_normal([EMBEDDING_DIM, ONE_HOT_DIM]))
    b2 = tf.Variable(tf.random_normal([1]))
    prediction = tf.nn.softmax(tf.add( tf.matmul(hidden_layer, W2), b2))

    # loss function: cross entropy
    loss = tf.reduce_mean(-tf.reduce_sum(y_label * tf.log(prediction), axis=[1]))

    # training operation
    train_op = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

    return train_op, loss, W1, b1, X_train, Y_train, x, y_label

def genskipgramdata(corpus, word2int):
    sentences = []
    data = []
    WINDOW_SIZE = 2

    for sentence in corpus:
        sentences.append(sentence.split())

    for sentence in sentences:
        for idx, word in enumerate(sentence):
            for neighbor in sentence[max(idx - WINDOW_SIZE, 0) : min(idx + WINDOW_SIZE, len(sentence)) + 1] : 
                if neighbor != word:
                    data.append([word, neighbor])
    
    return data


def convertword2int(words):
    word2int = {}
    for i,word in enumerate(words):
        word2int[word] = i
    
    return word2int

def remove_stop_words(corpus):
    stwords = ['is', 'a', 'will', 'be', 'on', 'to', 'as', 'the']
    out = []
    texto = ""

    for text in corpus:
        for word in re.split("\W+",text):
            if word not in stwords:
               texto += word + " "
        out.append(texto)
        texto = ""

    """
    for text in corpus:
        print(text)
        tmp = text.split(' ')

        for word in stwords:
            if word in tmp:
                tmp.remove(word)

        out.append(" ".join(tmp))
    """
    return out

def gettxtf(fname):
    out = []

    # Matches whitespace char \s + alphanumeric and underscore \w
    # Negative set [^ ] + OR _ |_
    # 1 or more +
    pattern = re.compile('([^\s\w]|_)+')

    with open(fname, "r") as fl:
        txt = fl.read().lower().replace("\n", "").replace(" ", ".")
        ls = txt.split(". ")
        for sen in ls:
            out.append(pattern.sub('', sen))

        print(out)
        return out

def cleantxt(text):
    # Matches whitespace char \s + alphanumeric and underscore \w
    # Negative set [^ ] + OR _ |_
    # 1 or more +
    pattern = re.compile('([^\s\w]|_)+')
    out = []

    txt = text.lower().replace("\n", "").replace(",", ".")
    ls = txt.split(". ")
    for sen in ls:
            out.append(pattern.sub('', sen))

    return out


def apiw2v(text, return_dict):
    #Get and clean text
    #corpus = gettxtf("testtxt.txt")
    corpus = cleantxt(text)
    corpus = remove_stop_words(corpus)

    words = []
    for text in corpus:
        for word in text.split(' '):
            words.append(word)

    words = list(filter(None, words))
    words = set(words)

    word2int = convertword2int(words)
    data = genskipgramdata(corpus, word2int)
    df = pd.DataFrame(data, columns = ['input', 'label'])

    train_op, loss, W1, b1, X_train, Y_train, x, y_label = computational_graph(words, word2int, data, df)
    vectors = train_data(train_op, X_train, Y_train, loss, W1, b1, x, y_label)

    out = matchvword(vectors, words)
    return_dict["w2v"] = out
    return return_dict


def multiprocw2v(text):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    p = multiprocessing.Process(target=apiw2v, args=(text, return_dict))
    p.start()

    p.join()
    return return_dict.values()[0]



if __name__ == "__main__":

    text = "A handful of major states resisted pressure on Sunday to ramp up efforts to combat global warming as a U.N. climate summit ground to a close, angering smaller countries and a growing protest movement that is pushing for emergency action.\
    The COP25 talks in Madrid were viewed as a test of governments' collective will to heed the advice of science to cut greenhouse gas emissions more rapidly, in order to prevent rising global temperatures from hitting irreversible tipping points.\
    But the conference, in its concluding draft, endorsed only a declaration on the \"urgent need\" to close the gap between existing emissions pledges and the temperature goals of the landmark 2015 Paris climate agreement - an outcome U.N. Secretary-General Antonio Guterres called disappointing.\
    Many developing countries and campaigners had wanted to see much more explicit language spelling out the importance of countries submitting bolder pledges on emissions as the Paris process enters a crucial implementation phase next year.\
    Irish restaurateurs are preparing to “go to war” with the insurance industry regarding disputes over policy payouts on foot of the coronavirus crisis.\
    With the country on full lockdown since March 27, the industry has been ravaged by an enforced lack of business.\
    However, an alleged blanket refusal on the part of industry insurers to recognise the pandemic as being cause for compensation per the terms of their contracts has led to increasing conflict between the sides.\
    A handful of major states resisted pressure on Sunday to ramp up efforts to combat global warming as a U.N. climate summit ground to a close, angering smaller countries and a growing protest movement that is pushing for emergency action.\
    The COP25 talks in Madrid were viewed as a test of governments' collective will to heed the advice of science to cut greenhouse gas emissions more rapidly, in order to prevent rising global temperatures from hitting irreversible tipping points.\
    But the conference, in its concluding draft, endorsed only a declaration on the \"urgent need\" to close the gap between existing emissions pledges and the temperature goals of the landmark 2015 Paris climate agreement - an outcome U.N. Secretary-General Antonio Guterres called disappointing.\
    Many developing countries and campaigners had wanted to see much more explicit language spelling out the importance of countries submitting bolder pledges on emissions as the Paris process enters a crucial implementation phase next year.\
    Irish restaurateurs are preparing to “go to war” with the insurance industry regarding disputes over policy payouts on foot of the coronavirus crisis.\
    With the country on full lockdown since March 27, the industry has been ravaged by an enforced lack of business.\
    However, an alleged blanket refusal on the part of industry insurers to recognise the pandemic as being cause for compensation per the terms of their contracts has led to increasing conflict between the sides."

    di = dict()
    o = multiprocw2v(text)
    print(o)
