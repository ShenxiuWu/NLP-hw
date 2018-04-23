
# coding: utf-8

# In[ ]:


import sys
import json
import time

#initialization
q = {}
NT = {}
unaryRule = {}
binaryRule = {}
words = set()


def grammarRules(counts_file):
    # read counts file got from question 4 to calculate parameters we need for CKY algorithm
    for l in open(counts_file):
        line = l.strip()
        if line:
            segments = line.split(" ")
            if "NONTERMINAL" in line: #Firstly we record all non-terminals & their counts in counts_file into a dic
                NT[segments[2]] = int(segments[0])
    for l in open(counts_file): # To calculate correctly, we need to take another for loop 
        line = l.strip()        # after above one has recorded all non-terminals
        if line:
            segments = line.split(" ")    
            if "UNARYRULE" in line: # According to the definition, parameter q(X->w) = Count(X->w)/Count(X)
                q[(segments[2], segments[3])] = float(segments[0])/NT[segments[2]]
                # add w to the unary rules dic of X
                if segments[2] not in unaryRule:
                    unaryRule[segments[2]] = {}
                if segments[3] not in unaryRule[segments[2]]:
                    unaryRule[segments[2]][segments[3]] = int(segments[0])
                words.add(segments[3])  # add w to the words set
            elif "BINARYRULE" in line: #According to the definition, parameter q(X->Y1Y2) = Count(X->Y1Y2)/Count(X)
                q[(segments[2], segments[3], segments[4])] = float(segments[0])/NT[segments[2]]
                # add (Y1, Y2) to the binary rules dic of X
                if segments[2] not in binaryRule:
                    binaryRule[segments[2]] = {}
                if (segments[3], segments[4]) not in binaryRule[segments[2]]:
                    binaryRule[segments[2]][(segments[3], segments[4])] = int(segments[0])
                                        
                    
def PCFG(sentence):
    pi = {}
    bp = {}

    # According to CKY algorithm, i & j belongs to {1...n}, thus, to align the sentence with i & j,
    # I add a star * to the head of sentence which makes the first character of sentence is s[1]
    star_sentence = ['*'] + sentence
    for i in range(1, len(sentence)+1): # check whether the word is unseen and if so, replace it with "_RARE_"
        if star_sentence[i] not in words:
            star_sentence[i] = "_RARE_"
    # Cky algorithm initialization pi(i,i,X) = q(X->xi)
    for i in range(1, len(sentence)+1):
        for X in unaryRule:
            if star_sentence[i] in unaryRule[X]:  # we need to firstly check whether the unary rule exists
                pi[(i,i,X)] = q[(X,star_sentence[i])]
    # Then beginning the CKY algorithm loop parts
    for l in range(1, len(sentence)):
        for i in range(1, len(sentence)-l+1):
            j = i + l
            for X in binaryRule:
                score_dic = {} # To store the probability of each combination
                for YZ in binaryRule[X]:
                    Y = YZ[0]
                    Z = YZ[1]
                    for s in range(i,j):
                        if ((i,s,Y) in pi and (s+1,j,Z) in pi):
                            result = q[(X,Y,Z)]*pi[(i,s,Y)]*pi[(s+1,j,Z)]
                            score_dic[(X,Y,Z,i,s,j)] = result
                if score_dic:
                    max_value = max(score_dic.values())
                    max_combination = [k for k, v in score_dic.items() if v == max_value]
                    pi[(i,j,X)] = max_value
                    temp = list(max_combination[0])
                    bp[(i,j,X)] = (temp[1],temp[2],temp[4])  # back pointer, record Y,Z,s
    
    mm = 0                   #Finally, we are expected to return pi[(1,n,'S')]. However, due to some of sentences 
    if (1,len(sentence),"S") not in pi: #in corpus are fragments, and they do not have 'S' as the root. 
        for X in NT:                    #Thus, if we cannot find pi[(1, n, 'S')], we should return the max value
            if (1,len(sentence),X) in pi: #on all non-terminals, i.e.return max pi[(1,n,X)], where X belongs to NT
                if pi[(1,len(sentence),X)] > mm:
                    mm = pi[(1,len(sentence),X)]
                    tbKey = (1,len(sentence),X)
    else:
        tbKey = (1,len(sentence),"S")
        
    return backtrace(tbKey, star_sentence, bp)
                    

def backtrace(tbKey, star_sentence, bp):  # Extract the tree from the backpointers we record.
    (i, j, X) = tbKey
    if i==j:
        return [X, star_sentence[i]]
    (Y,Z,s) = bp[(i,j,X)]
    return [X, backtrace((i,s,Y),star_sentence, bp), backtrace((s+1,j,Z),star_sentence, bp)]
       
    
def main(devFile,outputFile):
    with open (outputFile, 'w') as outputFile:
        for l in open(devFile):
            sentence = l.strip().split(" ")    
            tree = PCFG(sentence)
            outputFile.write("%s\n" % json.dumps(tree))     
                
def usage():
    sys.stderr.write("""
    Usage: firstly run: python parser.py q4 parse_train_vert.dat parse_train_vert.RARE.dat
        Then: python parser.py q6 parse_train_vert.RARE.dat parse_dev.dat q6_prediction_file
        The program is to use CKY algorithm parsing sentence in corpus_file.
        After getting prediction file, use: python eval_parser.py parse_dev.key q6_prediction_file > q6_eval.txt
        to evaluate the performance.\n""")
    
if __name__ == "__main__":
    time1 = time.time()
    if len(sys.argv) != 5:
        usage()
        sys.exit(1)
    grammarRules("parse_train_vert.RARE.counts")
    main(sys.argv[3], sys.argv[4])
    time2 = time.time()
    T = time2 - time1
    print("running time: ", T)

