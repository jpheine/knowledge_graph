"""This file contains the ExtractKnowledge Ability.
"""

import spacy
from spacy.matcher import Matcher

class ExtractKnowlegde():
    """This class is used to extracted knowledge as
    entity pairs from a sentence. The entity pairs
    can be further processed.
    """

    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def get_entities(self, sent : str) -> any:
        """Extracts knowledge out of a sentence. Therefore searches for subject object relations
        and stores them into an entity tuple.

        Args:
            sent (str): Sentence to be analyzed.

        Returns:
            any: Entity pair as tuple.
        """

        entity_1 = ""
        entity_2 = ""

        prv_tok_dep = ""    # dependency tag of previous token in the sentence
        prv_tok_text = ""   # previous token in the sentence

        prefix = ""         # If token is part of compound word (eg FOOTBALL (Prefix) Stadium)
        modifier = ""       # If token is part of modifier word (eg nice (modifier) Shirt)

        nlp_proc = self.nlp(sent)

        deps = [token.dep_ for token in nlp_proc]
        # limit graph to simple sentences with one subject and object
        if (deps.count('obj') + deps.count('dobj')) != 1\
                or (deps.count('subj') + deps.count('nsubj')) != 1:
            return

        for token in nlp_proc:

            # if token is a punctuation mark then move on to the next token
            if token.dep_ != "punct":
                # check: token is a compound word or not
                if token.dep_ == "compound":
                    prefix = token.text
                     # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                        prefix = prv_tok_text + " "+ token.text

                # check: token is a modifier or not
                if token.dep_.endswith("mod") == True:
                    modifier = token.text
                        # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                        modifier = prv_tok_text + " "+ token.text

                # If subject has been found add modifier and prefix to it
                if token.dep_.find("subj") == True:
                    entity_1 = modifier +" "+ prefix + " "+ token.text
                    prefix = ""
                    modifier = ""
                    prv_tok_dep = ""
                    prv_tok_text = ""

                # If object has been found add modifier and prefix to it
                if token.dep_.find("obj") == True:
                    entity_2 = modifier +" "+ prefix +" "+ token.text

                # update variables
                prv_tok_dep = token.dep_
                prv_tok_text = token.text

        return [entity_1.strip(), entity_2.strip()]

    def get_relation(self, sentence : str) -> str:
        """Searches for the relation between two entities (subject, object).
        Therefore, a search pattern is applied to the sentence.
        The search pattern can be modified as needed.

        Args:
            sentence (str): Sentence to be analyzed.

        Returns:
            str: relation between two entities.
        """

        doc = self.nlp(sentence)
        matcher = Matcher(self.nlp.vocab)

        # define the pattern
        # pattern tries to find the ROOT word for the main verb in the sentence
        # if ROOT is identified, the pattern checks whether it is followed by preposition (prep)
        # or agent word
        # if found, add it to the root word
        pattern = [ {'DEP':'ROOT'},
                    {'DEP':'prep','OP':"?"},
                    {'DEP':'agent','OP':"?"},
                    {'POS':'ADJ','OP':"?"}]

        # Search for the pattern
        matcher.add("matching_1", [pattern])

        #calc span
        matches = matcher(doc)
        k = len(matches) - 1

        span = doc[matches[k][1]:matches[k][2]]

        #return span text
        return span.text

    @staticmethod
    def filter_by_entitity_count(deps: any) -> bool:
        """This method filters a sentence by the number of contained
        and valid entities.
        If the entitiy count if subj. and obj. is other then 1, False will
        be returned.

        Args:
            deps (any): Token dependencies.

        Returns:
            bool: True, if sentence can be used, else false.
        """
        if (deps.count('obj') + deps.count('dobj')) != 1\
            or (deps.count('subj') + deps.count('nsubj')) != 1:
            return False
        return True
