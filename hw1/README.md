# NLP hw1 - Named Entity tagger with Viterbi algorithm

Quick View:

4_1.py: Replace infrequent words(Count(x) < 5) with a common symbol "_RARE_"

4_2.py: Implement a named entity tagger and make tag prediction base on emission rate

5_1.py: Print log probability for trigrams

5_2.py: Tag prediction using maximum likelihood estimates for transitions and emissions, Viterbi algorithm

6.py & 6_multiTag.py: Replace the rare words with different informative patterns, improved Viterbi algorithm performance


Summary: The target of the whole programming codes is to to build a trigram HMM tagger for named entities. The Viterbi algorithm is a dynamic programming algorithm which finds the maximum probability tag sequence for a series of predictions, based on emission and transition probabilities. In a Markov Process, emission is the probability of an output given a state and transition is the probability of transitioning to the state given the previous states. In our case, the emission parameter e(x|y) = the probability of the word being x given you attributed tag y. Now, our training data has 8286 counts of 'I-LOC' tags, 7 of which are the word 'Taipei' (this word really exists in ner_train.dat), e('Taipei'|'I-LOC') = 7/8286. Now with 10001 counts of 'I-ORG' tags, 1 of which is 'Taipei', e('Taipei'|'I-ORG') = 1/10001 which clearly lower than 7/8286. The transition parameter q(y<sub>i</sub> | y<sub>i-2</sub>, y<sub>i-1</sub>) = the probability of putting tag y in position i given it's two previous tags. This is calculated by Count(trigram)/Count(bigram). For each word in the development data, the Viterbi algorithm will associate a log-probability of the tagged sequence up to this word-tag combination based on the emission and transition parameters it obtained from the training data. It does this for every possible tag and adopts the more likely one. Clearly this won't be 100% correct as natural language is unpredictable, but this code is expected to get relatively high accuracy.


**Viterbi Algorithm Pseudocode**

(For each line in the [input_file]):

a. If the word is seen in training data (present in the wordCal dictionary, which contains the ratio of each tag of each word.), for each of the possible tags of the word:
  1. Calculate emission = wordCal[word][tag]
  2. Calculate transition = trigram_counts[trigram])/float(bigram_counts[bigram] Note: y<sub>i-2</sub> = *, y<sub>i-1</sub> = * for the first word of each sentence.
  3. Set probability = emission x transition
  4. Update max(probability) and arg max if needed.
  
b. If the word is not seen in the training data:
  1. Calculate emission = dic['_RARE_'][tag].
  2. Calculate q(y<sub>i</sub>|y<sub>i-2</sub>, y<sub>i-1</sub>) = trigram_counts[trigram])/float(bigram_counts[bigram]. Note: y<sub>i-2</sub> = ∗, y<sub>i-1</sub> = ∗ for the first word of each sentence
  3. Set probability = emission × transition
  4. Update max(probability) if needed, arg max = _RARE_
  
c. Write arg max and log(max(probability)) to output file.

d. Update y<sub>i-2</sub>, y<sub>i-1</sub>.

**Evaluation**

Prof. Michael Collins provided an evaluation script to verify the output of your Viterbi program implementation.
Usage: python eval_ne_tagger.py ner_dev.key prediction_file.
