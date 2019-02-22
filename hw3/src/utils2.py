#! /usr/bin/python2.7
from collections import defaultdict


class Vocab:
    def __init__(self, word_file, pos_file, labels_file,  actions_file):
        self.word_dict = {}
        self.pos_dict = {}
        self.labels_dict = {}
        self.actions_dict = {}

        for word_line in word_file.readlines():
            seg = word_line.strip().split(" ")
            self.word_dict[seg[0]] = int(seg[1])

        for pos_line in pos_file.readlines():
            seg = pos_line.strip().split(" ")
            self.pos_dict[seg[0]] = int(seg[1])

        for labels_line in labels_file.readlines():
            seg = labels_line.strip().split(" ")
            self.labels_dict[seg[0]] = int(seg[1])

        for actions_line in actions_file.readlines():
            seg = actions_line.strip().split(" ")
            self.actions_dict[seg[0]] = int(seg[1])


    def tagid2tag_str(self, id):
        return self.output_tags[id]

    def word2id(self, word):
        return self.word_dict[word] if word in self.word_dict else self.word_dict['<unk>']

    def pos2id(self, tag):
        return self.pos_dict[tag] if tag in self.pos_dict else self.pos_dict['<null>']

    def labels2id(self, label):
        return self.labels_dict[label] if label in self.labels_dict else self.labels_dict['<null>']

    def actions2id(self, action):
        return self.actions_dict[action]

    def num_words(self):
        return len(self.word_dict)

    def num_pos(self):
        return len(self.pos_dict)

    def num_labels(self):
        return len(self.labels_dict)

    def num_actions(self):
        return len(self.actions_dict)





