Name: Shenxiu Wu
UNI: sw3196 


---------------------------------------------------------
NLP - POS tagger with CKY algorithm
---------------------------------------------------------

See report.pdf for description and instructions.

PART 2: PERFORMANCE FOR ALGORITHM
---------------------------------
The running time of the algorithm is 0.54 seconds

PART 3: OBSERVATIONS AND COMMENTS ABOUT RESULTS
-----------------------------------------------
There are many infrequent words which are handled using _RARE_ tag. The output file shows this: ["S", ["NP", ["NOUN", "Ms."], ["NOUN", "_RARE_"]], ["S", ["VP", ["VERB", "plays"], ["NP+NOUN", "_RARE_"]], [".", "."]]]

PART 4: ADDITIONAL INFORMATION REQUESTED
----------------------------------------
The main information here is that execution call is inside parser.py and cfg.counts can now be generated through execution call inside files.


