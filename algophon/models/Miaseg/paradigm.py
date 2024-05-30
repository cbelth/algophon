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