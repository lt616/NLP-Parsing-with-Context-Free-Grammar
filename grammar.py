"""
COMS W4705 - Natural Language Processing - Fall 2018
Homework 2 - Parsing with Context Free Grammars 
Daniel Bauer
"""

import sys
from collections import defaultdict
from math import fsum 

class Pcfg(object): 
    """
    Represent a probabilistic context free grammar. 
    """

    def __init__(self, grammar_file): 
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None 
        self.read_rules(grammar_file)      
 
    def read_rules(self,grammar_file):
        
        for line in grammar_file: 
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line: 
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else: 
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()
                    
     
    def parse_rule(self,rule_s):
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";",1) 
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)

    def verify_grammar(self):
        """
        Return True if the grammar is a valid PCFG in CNF.
        Otherwise return False. 
        """
        # TODO, Part 1
         
        for key, value_array in self.lhs_to_rules.items(): 
            probs = [] 
            for value in value_array: 
                if not self.is_valid_left(key) or not self.is_valid_right(value[1]):
                    return False;
                probs.append(value[2]) 

            if abs(fsum(probs) - 1) > 0.000001: 
                return False 

        return True 


    # Helper function 
    def is_valid_left(self, key): 
        return self.is_nonterminal(key) 

    def is_valid_right(self, value): 
        if len(value) == 1: 
            return True 
        elif len(value) == 2: 
            return self.is_nonterminal(value[0]) and self.is_nonterminal(value[1]) 
        else: 
            return False 

    def is_nonterminal(self, value): 
        return value.isupper() 


if __name__ == "__main__":
    with open(sys.argv[1],'r') as grammar_file:
        grammar = Pcfg(grammar_file)
        print(grammar.verify_grammar()) 
        
