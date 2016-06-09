# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 17:00:00 2016
@author: Cory Taylor

Dependency parsing with spaCy
This script takes Unicode plain text and outputs its dependencies in CoNLL10
format. It was originally written to prepare input files for named/non-named 
entity extraction with xrenner (https://corpling.uis.georgetown.edu/xrenner/).

For spaCy installation instructions, see https://spacy.io/docs#getting-started.

"""

import spacy

# Load the English tagger
# Note: This step is expensive. The documentation (https://spacy.io/docs#english-init) 
# says it can take 10-20 seconds and 2-3 GB of RAM.
nlp = spacy.load('en')

text = u'''1. Cato's family got its first lustre and fame from his great-grandfather Cato (a man whose virtue gained him the greatest reputation and influence among the Romans, as has been written in his Life), but the death of both parents left him an orphan, together with his brother Caepio and his sister Porcia. Cato had also a half-sister, Servilia, the daughter of his mother.1 All these children were brought up in the home of Livius Drusus, their uncle on the mother's side, who at that time was a leader in the conduct of public affairs; for he was a most powerful speaker, in general a man of the greatest discretion, and yielded to no Roman in dignity of purpose.
[2] We are told that from his very childhood Cato displayed, in speech, in countenance, and in his childish sports, a nature that was inflexible, imperturbable, and altogether steadfast. He set out to accomplish his purposes with a vigour beyond his years, and while he was harsh and repellent to those who would flatter him, he was still more masterful towards those who tried to frighten him. It was altogether difficult to make him laugh, although once in a while he relaxed his features so far as to smile; and he was not quickly nor easily moved to anger, though once angered he was inexorable.'''

doc = nlp(text)

# CoNLL10 output
# SpaCy's output--in particular, its token IDs--takes some massaging in order 
#to produce a well-formed CoNLL10 document. 

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
        print(token_id + '\t' +      # token ID w/in sentence
              token_text + '\t' +    # token text
              lemma + '\t' +         # lemmatized token
              pos_tag + '\t' +       # part of speech tag for token
              pos_tag + '\t' +       # part of speech tag for token
              '_' + '\t' +           # placeholder for morphological information
              head_id + '\t' +       # ID of head token
              depend + '\t' +        # dependency function
              '_' + '\t' + '_')      # two unused columns