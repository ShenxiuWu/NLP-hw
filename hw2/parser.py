
# coding: utf-8

# In[ ]:


#! /usr/bin/python3

__author__="Shenxiu Wu <sw3196@.columbia.edu>"

import json
import sys
import time
import os

class q4:
    """
    Note: First run python count_cfg_freq.py parse_train.dat > cfg.counts
    with the original training data file    

    """    

    # A rare word can have more than one tag association. We need to see the whole dataset and 
    # determine how many times each word is occurring, irrespective of the tags.
    # For example, word "utilities" has 3 tags with each of them is {'NX+NOUN': 1, 'NOUN': 2, 'NP+NOUN': 2}. 
    # This means word "utilities" occurs 5 times in the entire dataset, thus it is not an infrequent word.
    def readfile(self, file): #This reads in the count file to identify _RARE_ words
        l = open(file, "r")
        record = {}
        for line in l:
            if "UNARYRULE" in line:
                segment = line.strip().split(" ")
                count = int(segment[0])
                word = segment[3]
                tag = segment[2]
                if word.strip("\n") in record:
                    record[word.strip("\n")] += count    
                else:
                    record[word.strip("\n")] = count
        w = [k for k, v in record.items()]
        c = [v for k, v in record.items()]
        rare_record = {}
        for i in range(len(c)): # Only keep infrequent words (Count(x) < 5) in record dic and input it into rare_record
            if c[i] < 5:
                rare_record[w[i]] = c[i]
        return rare_record    

    # Function "walk" goes through one tree, check each leaf(word) of the tree, if it's in rare_record, replace it with "_RARE_".
    def walk(self, tree, rare_record):
        if len(tree) == 3:
            self.walk(tree[1], rare_record)
            self.walk(tree[2], rare_record)
        else:
            if tree[1] in rare_record:
                tree[1] = "_RARE_"
        return tree    

    def search(self, countFile="cfg.counts"): #This function searches the JSON tree by going to leaves, if word in rare_record, replace it as _RARE_
        rare_record = self.readfile(countFile)
        with open (sys.argv[3], 'w') as outputFile:
            for l in open(sys.argv[2]):
                tree = json.loads(l)
                #Check all leaves of the tree, if word in rare_record, replace it as "_RARE_"
                result = self.walk(tree, rare_record)
                outputFile.write("%s\n" % json.dumps(result))    

    def usage(self):
        sys.stderr.write("""
        Usage: python parser.py q4 parse_train.dat parse_train.RARE.dat
            The program is to replace infrequent words (count < 5) with "_RARE_" in a corpus of trees.\n""")                



class q5_6:
    #initialization
    def __init__(self):
        self.q = {}
        self.NT = {}
        self.unaryRule = {}
        self.binaryRule = {}
        self.words = set()    
    

    def grammarRules(self, counts_file):
        # read counts file got from question 4 to calculate parameters we need for CKY algorithm
        for l in open(counts_file):
            line = l.strip()
            if line:
                segments = line.split(" ")
                if "NONTERMINAL" in line: #Firstly we record all non-terminals & their counts in counts_file into a dic
                    self.NT[segments[2]] = int(segments[0])
        for l in open(counts_file): # To calculate correctly, we need to take another for loop 
            line = l.strip()        # after above one has recorded all non-terminals
            if line:
                segments = line.split(" ")    
                if "UNARYRULE" in line: # According to the definition, parameter q(X->w) = Count(X->w)/Count(X)
                    self.q[(segments[2], segments[3])] = float(segments[0])/self.NT[segments[2]]
                    # add w to the unary rules dic of X
                    if segments[2] not in self.unaryRule:
                        self.unaryRule[segments[2]] = {}
                    if segments[3] not in self.unaryRule[segments[2]]:
                        self.unaryRule[segments[2]][segments[3]] = int(segments[0])
                    self.words.add(segments[3])  # add w to the words set
                elif "BINARYRULE" in line: #According to the definition, parameter q(X->Y1Y2) = Count(X->Y1Y2)/Count(X)
                    self.q[(segments[2], segments[3], segments[4])] = float(segments[0])/self.NT[segments[2]]
                    # add (Y1, Y2) to the binary rules dic of X
                    if segments[2] not in self.binaryRule:
                        self.binaryRule[segments[2]] = {}
                    if (segments[3], segments[4]) not in self.binaryRule[segments[2]]:
                        self.binaryRule[segments[2]][(segments[3], segments[4])] = int(segments[0])
                                            
                        
    def PCFG(self, sentence):
        pi = {}
        bp = {}    

        # According to CKY algorithm, i & j belongs to {1...n}, thus, to align the sentence with i & j,
        # I add a star * to the head of sentence which makes the first character of sentence is s[1]
        star_sentence = ['*'] + sentence
        for i in range(1, len(sentence)+1): # check whether the word is unseen and if so, replace it with "_RARE_"
            if star_sentence[i] not in self.words:
                star_sentence[i] = "_RARE_"
        # Cky algorithm initialization pi(i,i,X) = q(X->xi)
        for i in range(1, len(sentence)+1):
            for X in self.unaryRule:
                if star_sentence[i] in self.unaryRule[X]:  # we need to firstly check whether the unary rule exists
                    pi[(i,i,X)] = self.q[(X,star_sentence[i])]
        # Then beginning the CKY algorithm loop parts
        for l in range(1, len(sentence)):
            for i in range(1, len(sentence)-l+1):
                j = i + l
                for X in self.binaryRule:
                    score_dic = {} # To store the probability of each combination
                    for YZ in self.binaryRule[X]:
                        Y = YZ[0]
                        Z = YZ[1]
                        for s in range(i,j):
                            if ((i,s,Y) in pi and (s+1,j,Z) in pi):
                                result = self.q[(X,Y,Z)]*pi[(i,s,Y)]*pi[(s+1,j,Z)]
                                score_dic[(X,Y,Z,i,s,j)] = result
                    if score_dic:
                        max_value = max(score_dic.values())
                        max_combination = [k for k, v in score_dic.items() if v == max_value]
                        pi[(i,j,X)] = max_value
                        temp = list(max_combination[0])
                        bp[(i,j,X)] = (temp[1],temp[2],temp[4])  # back pointer, record Y,Z,s
        
        mm = 0                   #Finally, we are expected to return pi[(1,n,'S')]. However, due to some of sentences 
        if (1,len(sentence),"S") not in pi: #in corpus are fragments, and they do not have 'S' as the root. 
            for X in self.NT:                    #Thus, if we cannot find pi[(1, n, 'S')], we should return the max value
                if (1,len(sentence),X) in pi: #on all non-terminals, i.e.return max pi[(1,n,X)], where X belongs to NT
                    if pi[(1,len(sentence),X)] > mm:
                        mm = pi[(1,len(sentence),X)]
                        tbKey = (1,len(sentence),X)
        else:
            tbKey = (1,len(sentence),"S")
            
        return self.backtrace(tbKey, star_sentence, bp)
                            

    def backtrace(self, tbKey, star_sentence, bp):  # Extract the tree from the backpointers we record.
        (i, j, X) = tbKey
        if i==j:
            return [X, star_sentence[i]]
        (Y,Z,s) = bp[(i,j,X)]
        return [X, self.backtrace((i,s,Y),star_sentence, bp), self.backtrace((s+1,j,Z),star_sentence, bp)]
           
        
    def main(self, devFile,outputFile):
        with open (outputFile, 'w') as outputFile:
            for l in open(devFile):
                sentence = l.strip().split(" ")    
                tree = self.PCFG(sentence)
                outputFile.write("%s\n" % json.dumps(tree))     
                    
    def usage5(self):
        sys.stderr.write("""
        Usage: python parser.py q5 parse_train.RARE.dat parse_dev.dat q5_prediction_file
            The program is to use CKY algorithm parsing sentence in corpus_file.
            After getting prediction file, use: python eval_parser.py parse_dev.key q5_prediction_file > q5_eval.txt
            to evaluate the performance.\n""")

    def usage6(self):
        sys.stderr.write("""
        Usage: firstly run: python parser.py q4 parse_train_vert.dat parse_train_vert.RARE.dat
            Then: python parser.py q6 parse_train_vert.RARE.dat parse_dev.dat q6_prediction_file
            The program is to use CKY algorithm parsing sentence in corpus_file.
            After getting prediction file, use: python eval_parser.py parse_dev.key q6_prediction_file > q6_eval.txt
            to evaluate the performance.\n""")
        





if __name__ == "__main__":
    os.system("python2.7 count_cfg_freq.py "+ sys.argv[2] +"> cfg.counts")
    if sys.argv[1] == 'q4':
        q4 = q4()
        if len(sys.argv) != 4:
            q4.usage()
            sys.exit(4)
        q4.search()
    elif sys.argv[1] == 'q5':
        time1 = time.time()
        q5 = q5_6()
        if len(sys.argv) != 5:
            q5.usage5()
            sys.exit(5)
        q5.grammarRules("cfg.counts")
        q5.main(sys.argv[3], sys.argv[4])
        time2 = time.time()
        T = time2 - time1
        print("running time: " + str(T) + ' s')
    elif sys.argv[1] == 'q6':
        time1 = time.time()
        q6 = q5_6()
        if len(sys.argv) != 5:
            q6.usage6()
            sys.exit(6)
        q6.grammarRules("cfg.counts")
        q6.main(sys.argv[3], sys.argv[4])
        time2 = time.time()
        T = time2 - time1
        print("running time: " + str(T) + ' s')
    else:
        print("Refer to submission_guide_hw2.pdf firstly")


