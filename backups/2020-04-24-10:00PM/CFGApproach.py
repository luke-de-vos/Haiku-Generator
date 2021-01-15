import nltk
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import random

#from stackoverflow
#generate random sentence from passed grammar
def generate_sample(grammar, prod, frags):        
    if prod in grammar._lhs_index: # Derivation
        derivations = grammar._lhs_index[prod]            
        derivation = random.choice(derivations)            
        for d in derivation._rhs:            
            generate_sample(grammar, d, frags)
    elif prod in grammar._rhs_index:
        # terminal
        frags.append(str(prod))

grammar = nltk.CFG.fromstring("""
S -> NP | VP | NP VP
PP -> P N_S | P N_P
NP -> Det_S N_S | Det_P N_P
VP -> V_S Det_S N_S | V_P Det_P N_P
Det_S -> 'the' | 'my' | 'a'
Det_P -> 'the' | 'my' | 'these'
N_S -> 'leaf' | 'autumn' | 'winter' | 'sun' | 'wind'
N_P -> 'leaves ' | 'winds'
V_S -> 'sits' | 'lays' | 'laughs'
V_P -> 'sit' | 'lay' | 'laugh'
P -> 'in' | 'with' | 'on'
""")



frags = []  
generate_sample(grammar, grammar.start(), frags)
print(' '.join(frags))


#for sentence in generate(grammar, n=10):
#	print(' '.join(sentence))



