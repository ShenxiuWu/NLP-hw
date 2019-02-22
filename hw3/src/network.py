#! /usr/bin/python2.7
import dynet as dynet
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

class Network:
    def __init__(self, vocab, properties):
        self.properties = properties
        self.vocab = vocab

        # first initialize a computation graph container (or model).
        self.model = dynet.Model()

        # assign the algorithm for backpropagation updates.
        self.updater = dynet.AdamTrainer(self.model)

        # create embeddings for words, pos and label features.
        self.word_embedding = self.model.add_lookup_parameters((vocab.num_words(), properties.word_embed_dim))
        self.pos_embedding = self.model.add_lookup_parameters((vocab.num_pos(), properties.pos_embed_dim))
        self.label_embedding = self.model.add_lookup_parameters((vocab.num_labels(), properties.label_embed_dim))

        #create embeddings for glove.
        # gloveFile = "./src/glove.6B.200d.txt"
        # for line in open(gloveFile, 'r'):
        #     seg = line.strip().split(" ")
        #     if seg[0] in self.vocab.word_dict:
        #         vector = [float(s) for s in seg[1:]]
        #         self.word_embedding.init_row(self.vocab.word2id(seg[0]), vector)



        # assign transfer function
        self.transfer = dynet.rectify  # can be dynet.logistic or dynet.tanh as well.

        # define the input dimension for the embedding layer.
        # here we assume 20 word embeddings, 20 pos embeddings and 12 label embeddings.
        self.input_dim = 20 * properties.word_embed_dim + 20 * properties.pos_embed_dim + 12 * properties.label_embed_dim

        # define the hidden layer.
        self.hidden_first_layer = self.model.add_parameters((properties.hidden_first_dim, self.input_dim))
        self.hidden_second_layer = self.model.add_parameters((properties.hidden_second_dim, properties.hidden_first_dim))

        # define the hidden layer bias term and initialize it as constant 0.2.
        self.hidden_first_layer_bias = self.model.add_parameters(properties.hidden_first_dim, init=dynet.ConstInitializer(0.2))
        self.hidden_second_layer_bias = self.model.add_parameters(properties.hidden_second_dim, init=dynet.ConstInitializer(0.2))

        # define the output weight.
        self.output_layer = self.model.add_parameters((vocab.num_actions(), properties.hidden_second_dim))

        # define the bias vector and initialize it as zero.
        self.output_bias = self.model.add_parameters(vocab.num_actions(), init=dynet.ConstInitializer(0))

    def build_graph(self, features, dropout=False):
        # extract word, pos and labels ids
        word_ids = [self.vocab.word2id(word) for word in features[0:20]]
        pos_ids = [self.vocab.pos2id(pos) for pos in features[20:40]]
        label_ids = [self.vocab.labels2id(label) for label in features[40:52]]

        # extract word embeddings and tag embeddings from features
        word_embeds = [self.word_embedding[wid] for wid in word_ids]
        pos_embeds = [self.pos_embedding[tid] for tid in pos_ids]
        label_embeds = [self.label_embedding[tid] for tid in label_ids]

        # concatenating all features (recall that '+' for lists is equivalent to appending two lists)
        embedding_layer = dynet.concatenate(word_embeds + pos_embeds + label_embeds)
        
        # Below I set the dropout parameter, this is a try from part 3.
        p = 0.25
        # if dropout:
        #     embedding_layer = dynet.dropout(embedding_layer, p)

        # calculating the 2 hidden layers
        # .expr() converts a parameter to a matrix expression in dynet (its a dynet-specific syntax).
        hidden_one = self.transfer(self.hidden_first_layer.expr() * embedding_layer + self.hidden_first_layer_bias.expr())
        # if dropout:
        #     hidden_one = dynet.dropout(hidden_one, p)

        hidden_two = self.transfer(self.hidden_second_layer.expr() * hidden_one + self.hidden_second_layer_bias.expr())
        # if dropout:
        #     hidden_two = dynet.dropout(hidden_two, p)

        # calculating the output layer
        output = self.output_layer.expr() * hidden_two + self.output_bias.expr()

        # return the output as a dynet vector (expression)
        return output

    def train(self, train_file, epochs):
        # matplotlib config
        loss_values = []
        # plt.ion()
        # ax = plt.gca()
        # ax.set_xlim([0, 10])
        # ax.set_ylim([0, 3])
        # plt.title("Loss over time")
        # plt.xlabel("Minibatch")
        # plt.ylabel("Loss")

        for i in range(epochs):
            print ('started epoch', (i+1))
            losses = []
            train_data = open(train_file, 'r').read().strip().split('\n')

            # shuffle the training data.
            random.shuffle(train_data)

            step = 0
            for line in train_data:
                fields = line.strip().split(' ')
                features, label = fields[:-1], fields[-1]
                gold_label = self.vocab.actions2id(label)
                result = self.build_graph(features)

                # getting loss with respect to negative log softmax function and the gold label.
                loss = dynet.pickneglogsoftmax(result, gold_label)

                # appending to the minibatch losses
                losses.append(loss)
                step += 1

                if len(losses) >= self.properties.minibatch_size:
                    # now we have enough loss values to get loss for minibatch
                    minibatch_loss = dynet.esum(losses) / len(losses)

                    # calling dynet to run forward computation for all minibatch items
                    minibatch_loss.forward()

                    # getting float value of the loss for current minibatch
                    minibatch_loss_value = minibatch_loss.value()

                    # printing info and plotting
                    loss_values.append(minibatch_loss_value)
                    if len(loss_values)%10==0:
                        # ax.set_xlim([0, len(loss_values)+10])
                        # ax.plot(loss_values)
                        # plt.draw()
                        # plt.pause(0.0001)
                        progress = round(100 * float(step) / len(train_data), 2)
                        print ('current minibatch loss', minibatch_loss_value, 'progress:', progress, '%')

                    # calling dynet to run backpropagation
                    minibatch_loss.backward()

                    # calling dynet to change parameter values with respect to current backpropagation
                    self.updater.update()

                    # empty the loss vector
                    losses = []

                    # refresh the memory of dynet
                    dynet.renew_cg()

            # there are still some minibatch items in the memory but they are smaller than the minibatch size
            # so we ask dynet to forget them
            dynet.renew_cg()

    def decode(self, words):
        # first putting two start symbols
        words = ['<s>', '<s>'] + words + ['</s>', '</s>']
        tags = ['<s>', '<s>']

        for i in range(2, len(words) - 2):
            features = words[i - 2:i + 3] + tags[i - 2:i]

            # running forward
            output = self.build_graph(features)

            # getting list value of the output
            scores = output.npvalue()

            # getting best tag
            best_tag_id = np.argmax(scores)

            # assigning the best tag
            tags.append(self.vocab.tagid2tag_str(best_tag_id))

            # refresh dynet memory (computation graph)
            dynet.renew_cg()

        return tags[2:]

    def load(self, filename):
        self.model.populate(filename)

    def save(self, filename):
        self.model.save(filename)
