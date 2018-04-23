Name-Animesh Anant Sharma
UNI-aas2325


---------------------------------------------------------
Question 4:
---------------------------------------------------------
4:
PART 1: HOW TO RUN CODE
-----------------------
The following command can be used to get output in parse_train.RARE.dat
python parser.py q4 parse_train.dat parse_train.RARE.dat

PART 2: PERFORMANCE FOR ALGORITHM
---------------------------------
The running time of the algorithm is 0.54 seconds

PART 3: OBSERVATIONS AND COMMENTS ABOUT RESULTS
-----------------------------------------------
There are many infrequent words which are handled using _RARE_ tag. The output file shows this: ["S", ["NP", ["NOUN", "Ms."], ["NOUN", "_RARE_"]], ["S", ["VP", ["VERB", "plays"], ["NP+NOUN", "_RARE_"]], [".", "."]]]

PART 4: ADDITIONAL INFORMATION REQUESTED
----------------------------------------
The main information here is that execution call is inside parser.py and cfg.counts can now be generated through execution call inside files.



---------------------------------------------------------
Question 5:
---------------------------------------------------------
5:
PART 1: HOW TO RUN CODE
-----------------------
The prediction file is obtained using parser.py.
python parser.py q5 parse_train.RARE.dat parse_dev.dat q5_prediction_file
The evaluation file q5_eval is obtained using:
python eval_parser.py parse_dev.key q5_prediction_file > q5_eval.txt

PART 2: PERFORMANCE FOR ALGORITHM
---------------------------------
CKY algorithm:
      Type       Total   Precision      Recall     F1 Score
===============================================================
         .         370     1.000        1.000        1.000
       ADJ         164     0.827        0.555        0.664
      ADJP          29     0.333        0.241        0.280
  ADJP+ADJ          22     0.542        0.591        0.565
       ADP         204     0.955        0.946        0.951
       ADV          64     0.694        0.531        0.602
      ADVP          30     0.333        0.133        0.190
  ADVP+ADV          53     0.756        0.642        0.694
      CONJ          53     1.000        1.000        1.000
       DET         167     0.988        0.976        0.982
      NOUN         671     0.752        0.842        0.795
        NP         884     0.632        0.529        0.576
    NP+ADJ           2     0.286        1.000        0.444
    NP+DET          21     0.783        0.857        0.818
   NP+NOUN         131     0.641        0.573        0.605
    NP+NUM          13     0.214        0.231        0.222
   NP+PRON          50     0.980        0.980        0.980
     NP+QP          11     0.667        0.182        0.286
       NUM          93     0.984        0.645        0.779
        PP         208     0.588        0.625        0.606
      PRON          14     1.000        0.929        0.963
       PRT          45     0.957        0.978        0.967
   PRT+PRT           2     0.400        1.000        0.571
        QP          26     0.647        0.423        0.512
         S         587     0.626        0.782        0.695
      SBAR          25     0.091        0.040        0.056
      VERB         283     0.683        0.799        0.736
        VP         399     0.559        0.594        0.576
   VP+VERB          15     0.250        0.267        0.258

     total        4664     0.714        0.714        0.714
The execution time is 56 seconds.

PART 3: OBSERVATIONS AND COMMENTS ABOUT RESULTS
-----------------------------------------------
The performance is really good for tags like ., DET, ADP, NP+PRON, NUM, PRON and the model does not perform well for tags like ADJP, VP+VERB, SBAR, NP+NUM, ADVP. The model is able to perform reasonably well for specific tags but it is not able to generalise well to normal POS tags like VP,PP,NP+NOUN.

PART 4: ADDITIONAL INFORMATION REQUESTED
----------------------------------------
The cfg.counts file is generated inside program and input and output files are specified through parser.py.



---------------------------------------------------------
Question 6:
---------------------------------------------------------
6:
PART 1: HOW TO RUN CODE
-----------------------
The RARE counts file is obtained using:
python parser.py q4 parse_train_vert.dat parse_train_vert.RARE.dat
The prediction file is obtained using:
python parser.py q6 parse_train_vert.RARE.dat parse_dev.dat q6_prediction_file
The evaluation is obtained using:
python eval_parser.py parse_dev.key q6_prediction_file > q6_eval.txt

PART 2: PERFORMANCE FOR ALGORITHM
---------------------------------
CKY algorithm using markovization:
      Type       Total   Precision      Recall     F1 Score
===============================================================
         .         370     1.000        1.000        1.000
       ADJ         164     0.689        0.622        0.654
      ADJP          29     0.324        0.414        0.364
  ADJP+ADJ          22     0.591        0.591        0.591
       ADP         204     0.960        0.951        0.956
       ADV          64     0.759        0.641        0.695
      ADVP          30     0.417        0.167        0.238
  ADVP+ADV          53     0.700        0.660        0.680
      CONJ          53     1.000        1.000        1.000
       DET         167     0.988        0.994        0.991
      NOUN         671     0.795        0.845        0.819
        NP         884     0.617        0.548        0.580
    NP+ADJ           2     0.333        0.500        0.400
    NP+DET          21     0.944        0.810        0.872
   NP+NOUN         131     0.610        0.656        0.632
    NP+NUM          13     0.375        0.231        0.286
   NP+PRON          50     0.980        0.980        0.980
     NP+QP          11     0.750        0.273        0.400
       NUM          93     0.914        0.688        0.785
        PP         208     0.623        0.635        0.629
      PRON          14     1.000        0.929        0.963
       PRT          45     1.000        0.933        0.966
   PRT+PRT           2     0.286        1.000        0.444
        QP          26     0.650        0.500        0.565
         S         587     0.704        0.814        0.755
      SBAR          25     0.667        0.400        0.500
      VERB         283     0.790        0.813        0.801
        VP         399     0.663        0.677        0.670
   VP+VERB          15     0.294        0.333        0.312

     total        4664     0.742        0.742        0.742
The execution time is 99 seconds.

PART 3: OBSERVATIONS AND COMMENTS ABOUT RESULTS
-----------------------------------------------
The markovization helps in improving performance for prediction of general tags like NOUN, ADVP, ADV while at the same time there is decrement in preformance of prediction of tags like ADVP+ADV, ADJP but the decrement is slight. The modification is not able to further improve the performance of specific tags like NUM and PRT+PRT. 

The main thing to note here is that is significant improvement in prediction of SBAR from 0.091 to 0.667. This is due to determination of parent nodes and then associating these parents with their children. 

One specific example where the performance improved can be:
The sentence is:
Conversation was subdued as most patrons watched the latest market statistics on television .

The correct output is:
["S", ["NP+NOUN", "Conversation"], ["S", ["VP", ["VERB", "was"], ["VP", ["ADJP+ADJ", "subdued"], ["SBAR", ["ADP", "as"], ["S", ["NP", ["ADJ", "most"], ["NOUN", "patrons"]], ["VP", ["VERB", "watched"], ["VP", ["NP", ["DET", "the"], ["NP", ["ADJ", "latest"], ["NP", ["NOUN", "market"], ["NOUN", "statistics"]]]], ["PP", ["ADP", "on"], ["NP+NOUN", "television"]]]]]]]], [".", "."]]]

The output from normal CKY is:
["S", ["VP", ["VERB", "Conversation"], ["VP", ["VERB", "was"], ["VP", ["VERB", "subdued"], ["VP", ["ADV", "as"], ["VP", ["ADV", "most"], ["VP", ["VERB", "patrons"], ["VP", ["VERB", "watched"], ["NP", ["DET", "the"], ["NP", ["ADJ", "latest"], ["NP", ["NP", ["NOUN", "market"], ["NOUN", "statistics"]], ["PP", ["ADP", "on"], ["NP+NOUN", "television"]]]]]]]]]]]], [".", "."]]

The output after markovization is:
["S", ["VP^<S>", ["VERB", "Conversation"], ["VP^<VP>", ["VERB", "was"], ["VP", ["ADJP^<VP>+ADJ", "subdued"], ["SBAR^<VP>", ["ADP", "as"], ["S^<SBAR>", ["NP^<S>", ["ADJ", "most"], ["NOUN", "patrons"]], ["VP^<S>", ["VERB", "watched"], ["NP^<VP>", ["NP^<NP>", ["DET", "the"], ["NP", ["ADJ", "latest"], ["NP", ["NOUN", "market"], ["NOUN", "statistics"]]]], ["PP^<NP>", ["ADP", "on"], ["NP^<PP>+NOUN", "television"]]]]]]]]], [".", "."]]

So we see that SBAR prediction is done poorly in normal CKY implementation.

PART 4: ADDITIONAL INFORMATION REQUESTED
----------------------------------------
The performance improves after markovization from 71.4 to 74.2 percent.

