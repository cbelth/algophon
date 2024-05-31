from typing import Union

from algophon import SegStr

class Paradigm:
    '''
    A lightweight class representing a morphological paradigm, namely a uniquely-identifying root and a set of words.
    '''
    def __init__(self, root: str) -> object:
        '''
        :root: a str uniquely identifying the paradigm (e.g., a lemma or a unique id)
            - The form of the root is never used
        '''
        self.root = root
        self.words = set()

    def __str__(self) -> str:
        return self.root
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self.words)
    
    def add_word(self, word: Union[str, SegStr], features: tuple) -> None:
        '''
        :word: a str or SegStr object
        :features: a tuple of features marked in the word
        '''
        self.words.add((word, features))

    def get_one_diff_pairs(self) -> list[dict]:
        '''
        Computes the list of pairs (w1, w2) of words in the paradigm that differ in exactly one feature.
        A difference is either of:
            (1) a feature that w1 has but w2 does not
            (2) a feature that w2 has but w1 does not

        :return: list of pairs of words differing in exactly one feature
            - each entry is a dictionary:
                - 'src': the word with one fewer feature
                - 'tgt': the word with one more feature
                - 'feat': the feture that 'tgt' adds to 'src'
                - 'shared_feats': the features that 'src' and 'tgt' share
        '''
        one_diff = list() # init list
        words = sorted(self.words)
        for i in range(len(words)): # iterate over words
            for j in range(i + 1, len(words)): # iterate over other words
                w1, f1 = words[i]
                w2, f2 = words[j]
                union = set(f1).union(f2) # compute union of features
                intersection = set(f1).intersection(f2) # compute intersection of features
                diff = union.difference(intersection)
                if len(diff) == 1:
                    # add w1 -> w2 if f2 > f1 or add w2 -> w1 if f1 > f2
                    src, tgt = (w1, w2) if len(f1) < len(f2) else (w2, w1)
                    one_diff.append({ # build dict
                        'src': src, 
                        'tgt': tgt,
                        'feat': list(diff)[0],
                        'shared_feats': intersection,
                    })
        return one_diff