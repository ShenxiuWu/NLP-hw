#! /usr/bin/python2.7
import os,sys
from net_properties import *
from utils2 import *
from network import *
import pickle

#Then we begin to set properties and train the model.
word_embed_dim = 64
pos_embed_dim = 32
label_embed_dim = 32
hidden_first_dim = 200
hidden_second_dim = 200
minibatch_size = 1000
epochs = 7
NetProp = NetProperties(word_embed_dim, pos_embed_dim, label_embed_dim, hidden_first_dim, hidden_second_dim, minibatch_size)
#open file
word_file = open("../data/vocabs.word", "r")
pos_file = open("../data/vocabs.pos", "r")
labels_file = open("../data/vocabs.labels", "r")
actions_file = open("../data/vocabs.actions", "r")
vocab = Vocab(word_file, pos_file, labels_file, actions_file)
network = Network(vocab, NetProp)
pickle.dump((vocab, NetProp), open("../data/pkl1", 'w'))
network.train("../data/train.data", epochs)
network.save("../data/model1")
