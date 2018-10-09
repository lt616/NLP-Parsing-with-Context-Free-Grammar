"""
COMS W4705 - Natural Language Processing - Fall 2018
Homework 2 - Parsing with Context Free Grammars 
Daniel Bauer
"""
import math
import sys
from collections import defaultdict
import itertools
from grammar import Pcfg

### Use the following two functions to check the format of your data structures in part 3 ###
def check_table_format(table):
    """
    Return true if the backpointer table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Backpointer table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and \
          isinstance(split[0], int)  and isinstance(split[1], int):
            sys.stderr.write("Keys of the backpointer table must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of backpointer table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            bps = table[split][nt]
            if isinstance(bps, str): # Leaf nodes may be strings
                continue 
            if not isinstance(bps, tuple):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Incorrect type: {}\n".format(bps))
                return False
            if len(bps) != 2:
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Found more than two backpointers: {}\n".format(bps))
                return False
            for bp in bps: 
                if not isinstance(bp, tuple) or len(bp)!=3:
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has length != 3.\n".format(bp))
                    return False
                if not (isinstance(bp[0], str) and isinstance(bp[1], int) and isinstance(bp[2], int)):
                    print(bp)
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has incorrect type.\n".format(bp))
                    return False
    return True

def check_probs_format(table):
    """
    Return true if the probability table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Probability table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and isinstance(split[0], int) and isinstance(split[1], int):
            sys.stderr.write("Keys of the probability must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of probability table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            prob = table[split][nt]
            if not isinstance(prob, float):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a float.{}\n".format(prob))
                return False
            if prob > 0:
                sys.stderr.write("Log probability may not be > 0.  {}\n".format(prob))
                return False
    return True



class CkyParser(object):
    """
    A CKY parser.
    """

    def __init__(self, grammar): 
        """
        Initialize a new parser instance from a grammar. 
        """
        self.grammar = grammar

    def is_in_language(self,tokens):
        """
        Membership checking. Parse the input tokens and return True if 
        the sentence is in the language described by the grammar. Otherwise
        return False
        """
        # TODO, part 2 

        n = len(tokens) 

        cky_table = {} 
        for i in range(0, n): 
            cky_table[i] = {} 
            for j in range(i + 1, n + 1): 
                cky_table[i][j] = [] 
                if i + 1 == j: 
                    for A in self.grammar.rhs_to_rules[tuple([tokens[i]])]: 
                        cky_table[i][j].append(A[0]) 
                        # print(A[0]) 

        # print(cky_table) 

        for length in range(2, n + 1): 
            for i in range(0, n - length + 1): 
                j = i + length 
                for k in range(i + 1, j): 
                    # if not cky_table[i][k] or not cky_table[k][j]: 
                    #     continue; 

                    for B in cky_table[i][k]: 
                        for C in cky_table[k][j]: 
                            for A in self.grammar.rhs_to_rules[tuple([B, C])]:  
                                cky_table[i][j].append(A[0])  
                                # print(A[0] + "->" + B + " " + C)  


        return not not cky_table[0][n]  
       
    def parse_with_backpointers(self, tokens):
        """
        Parse the input tokens and return a parse table and a probability table.
        """
        # TODO, part 3 

        n = len(tokens) 

        table = {} 
        probs = {} 

        for i in range(0, n): 
            for j in range(i + 1, n + 1): 
                table[tuple([i, j])] = {}
                if i + 1 == j: 
                    for A in self.grammar.rhs_to_rules[tuple([tokens[i]])]: 
                        table[tuple([i, j])][A[0]] = tokens[i]  

        for i in range(0, n): 
            for j in range(i + 1, n + 1): 
                probs[tuple([i, j])] = {}
                if i + 1 == j: 
                    for A in self.grammar.rhs_to_rules[tuple([tokens[i]])]: 
                        probs[tuple([i, j])][A[0]] = math.log(A[2])  
                        print(math.log(A[2])) 

        for length in range(2, n + 1): 
            for i in range(0, n - length + 1): 
                j = i + length 
                for k in range(i + 1, j): 

                    for B in table[tuple([i, k])]: 
                        for C in table[tuple([k, j])]: 
                            for A in self.grammar.rhs_to_rules[tuple([B, C])]:  
                                table[tuple([i, j])][A[0]] = tuple([tuple([B, i, k]), tuple([C, k, j])]) 

        for length in range(2, n + 1): 
            for i in range(0, n - length + 1): 
                j = i + length 
                for k in range(i + 1, j): 

                    for B in probs[tuple([i, k])]: 
                        for C in probs[tuple([k, j])]: 
                            for A in self.grammar.rhs_to_rules[tuple([B, C])]:  
                                probs[tuple([i, j])][A[0]] = math.log(A[2]) + probs[tuple([i, k])][B] + probs[tuple([k, j])][C]  

        print(check_table_format(table)) 
        print(check_probs_format(probs)) 

        return table, probs


def get_tree(chart, i,j,nt): 
    """
    Return the parse-tree rooted in non-terminal nt and covering span i,j.
    """
    # TODO: Part 4 

    current = chart[tuple([i, j])][nt] 
    if not isinstance(current, tuple):  
        return tuple([nt, current]) 
    else: 
        B = current[0] 
        C = current[1] 
        # print(get_tree(chart, B[1], B[2], B[0])) 
        # print(get_tree(chart, C[1], C[2], C[0])) 
        return tuple([nt, get_tree(chart, B[1], B[2], B[0]), get_tree(chart, C[1], C[2], C[0])])


       
if __name__ == "__main__":
    
    with open('atis3.pcfg','r') as grammar_file: 
        grammar = Pcfg(grammar_file) 
        print(grammar.rhs_to_rules[('flights',)])  
        parser = CkyParser(grammar)
        toks =['flights', 'from','miami', 'to', 'cleveland','.'] 
        # toks =['miami', 'flights','cleveland', 'from', 'to','.'] 
        print(parser.is_in_language(toks))
        table,probs = parser.parse_with_backpointers(toks) 
        print(get_tree(table, 0, len(toks), grammar.startsymbol)) 
        #assert check_table_format(chart)
        #assert check_probs_format(probs)
        
