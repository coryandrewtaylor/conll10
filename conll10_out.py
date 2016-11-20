#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
conll10_out.py

Purpose: Dependency parsing with spaCy

This script takes Unicode plain text and outputs its dependencies in 
CoNLL10 format. It was originally written to prepare input files for 
named/non-named entity extraction with xrenner
(https://corpling.uis.georgetown.edu/xrenner/).

For installation instructions for spaCy, see 
https://spacy.io/docs#getting-started.
'''

import spacy
import os
from os.path import join as pjoin

print('conll10_out.py')

def main(files):
    print('Loading spaCy...')
    nlp = spacy.load('en')
    
    for filename in files:
        print('Processing ' + filename)
        input_txt = pjoin(os.sep, input_dir, filename)
        output_conll10 = (pjoin(os.sep, output_dir, filename[:-4]) 
                          + '_out' + os.extsep + 'conll10')
        output_txt = pjoin(os.sep, output_dir, filename)
        
        clean_up_file(output_conll10)
        clean_up_file(output_txt)
        
        conll(nlp, input_txt, output_conll10)
        
        os.rename(input_txt, output_txt)

def clean_up_file(file):
    if os.path.isfile(file):
        os.remove(file)
        
def conll(nlp, input_file, output_file):
    with open(input_file, 'r') as input_text:
        text = input_text.read()#.decode('utf-8')
        
    '''Load and run the English tagger
    Note: Loading the tagger is expensive. The documentation (https://spacy.io/
    docs#english-init) says it can take 10-20 seconds and 2-3 GB of RAM.'''
    doc = nlp(text)
        
        
    '''CoNLL10 output
    SpaCy's output--in particular, its token IDs--takes some massaging in 
    order to produce a well-formed CoNLL10 document. 
    The column layout is described at https://corpling.uis.georgetown.edu/
    xrenner/doc/using.html#input-format.'''
    with open(output_file, 'w') as output:
        for sent in doc.sents:
            # Create lookup dict for token IDs.
            ids = {}
            for i, token in enumerate(sent):
                ids[token.idx] = i+1
                
            for token in sent:
                # Clean up token attributes
                token_id = str(ids[token.idx]).strip()
                token_text = str(token).strip()
                lemma = str(token.lemma_).strip()
                pos_tag = str(token.tag_).strip()
                depend = str(token.dep_).strip()
                
                # Set head ID correctly for root of sentence.
                if token.dep_ == 'ROOT':
                    head_id = str(0)
                else:
                    head_id = str(ids[token.head.idx]).strip()
                    
                # CoNLL10 output
                # Comments below are modified from https://corpling.uis.georgetown.edu/
                # xrenner/doc/using.html#input-format
                output.write(
                token_id + '\t' +      # token ID w/in sentence
                token_text + '\t' +    # token text
                lemma + '\t' +         # lemmatized token
                pos_tag + '\t' +       # part of speech tag for token
                pos_tag + '\t' +       # part of speech tag for token
                '_' + '\t' +           # placeholder for morphological information
                head_id + '\t' +       # ID of head token
                depend + '\t' +        # dependency function
                '_' + '\t' +           # unused column
                '_' + '\n')            # unused column

input_dir = pjoin(os.sep, os.getcwd(), 'input')
output_dir = pjoin(os.sep, os.getcwd(), 'output')

input_files = []

for path, subdirs, files in os.walk(input_dir):
    for filename in files:
        if path == input_dir and filename.lower().endswith('.txt'):
            input_files.append(filename)

if len(input_files) > 0:
    main(input_files)
else:
    print('No .txt files in root of input directory. Exiting.')