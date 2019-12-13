import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# import tensorflow as tf 
# AttributeError: 'module' object has no attribute 'placeholder'
# use api 1 as is removed in 2
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

def matchvword(vectors, words): 
    df = pd.DataFrame(vectors, columns = ['x1', 'x2'])
    df['word'] = words
    df = df[['word', 'x1', 'x2']]

    return df

    
def train_data(train_op, X_train, Y_train, loss, W1, b1, x, y_label):
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init) 

    iteration = 20000
    for i in range(iteration):
        # input is X_train which is one hot encoded word
        # label is Y_train which is one hot encoded neighbor word
        sess.run(train_op, feed_dict={x: X_train, y_label: Y_train})
        if i % 3000 == 0:
            print('iteration '+str(i)+' loss is : ', sess.run(loss, feed_dict={x: X_train, y_label: Y_train}))

    # Now the hidden layer (W1 + b1) is actually the word look up table
    vectors = sess.run(W1 + b1)

    return vectors


# function to convert numbers to one hot vectors
def to_one_hot_encoding(data_point_index, ONE_HOT_DIM):
    one_hot_encoding = np.zeros(ONE_HOT_DIM)
    one_hot_encoding[data_point_index] = 1
    return one_hot_encoding

def computational_graph(words, word2int, data):
    ONE_HOT_DIM = len(words)
    X = [] # input word
    Y = [] # target word

    for x, y in zip(df['input'], df['label']):
        X.append(to_one_hot_encoding(word2int[ x ], ONE_HOT_DIM))
        Y.append(to_one_hot_encoding(word2int[ y ], ONE_HOT_DIM))

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
    for text in corpus:
        tmp = text.split(' ')

        for word in stwords:
            if word in tmp:
                tmp.remove(word)

        out.append(" ".join(tmp))
    
    return out

def gettxt(fname):
    out = []
    pattern = re.compile('([^\s\w]|_)+')
    with open(fname, "r") as fl:
        txt = fl.read().lower().replace("\n", "").replace(",", ".")
        ls = txt.split(".")
        for sen in ls:
            out.append(pattern.sub('', sen))

        print(out)
        return out


#Get and clean text
corpus = gettxt("testtxt.txt")
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

train_op, loss, W1, b1, X_train, Y_train, x, y_label = computational_graph(words, word2int, data)
vectors = train_data(train_op, X_train, Y_train, loss, W1, b1, x, y_label)

out = matchvword(vectors, words)
print(out)

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for word, x1, x2 in zip(out['word'], out['x1'], out['x2']):
    ax.annotate(word, (x1,x2 ))
    
PADDING = 1.0
x_axis_min = np.amin(vectors, axis=0)[0] - PADDING
y_axis_min = np.amin(vectors, axis=0)[1] - PADDING
x_axis_max = np.amax(vectors, axis=0)[0] + PADDING
y_axis_max = np.amax(vectors, axis=0)[1] + PADDING
 
plt.xlim(x_axis_min,x_axis_max)
plt.ylim(y_axis_min,y_axis_max)
plt.rcParams["figure.figsize"] = (10,10)

plt.show()