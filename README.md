# NLP-Parsing-with-Context-Free-Grammar
Build a CNF(Context Free Grammar) parse machine using CKY(Cocke-Kasami-Younger) algorithm, which is a bottom up DP algorithm. 
The basic interface and data are provided by prof. Daniel Bauer.  

# Dataset 
The main data for this project has been extracted from the ATIS (Air Travel Information Services) subsection of the Penn Treebank. ATIS is originally a spoken language corpus containing user queries about air travel. These queries have been transcribed into text and annotated with Penn-Treebank phrase structure syntax.
The data set contains sentences such as  "what is the price of flights from indianapolis to memphis ." 

There were 576 sentences in total, out of which 518 were used for training (extracting the grammar and probabilites) and 58 for test. The data set is obviously tiny compared to the entire Penn Treebank and typically that would not be enough training data. However, because the domain is so restricted, the extracted grammar is actually able to generalize reasonably well to the test data. 

# Implementation 
* ```def CkyParser(grammar) ``` return True if the grammar can parse this sentence and False otherwise. 

* ```def parser.parse_with_backpointers(toks) ``` The method should take a list of tokens as input and returns a) the parse table b) a probability table. 

* ```def get_tree(table, 0, len(toks), grammar.startsymbol) ``` return the parse-tree rooted in non-terminal nt and covering span i,j. 

# Performance Evaluation 
* Coverage: 67.24% 
* Average F-score (parsed sentences): 0.9504475408614075 
* Average F-score (all sentences): 0.6390940360964636 
