from typing import Hashable, Iterable, Union
from algophon import SegStr

class Miaseg:
    '''
    '''
    def __init__(self):
        pass

    def __str__(self) -> str:
        return 'Mɪᴀꜱᴇɢ'
    
    def __repr__(self) -> str:
        return self.__str__()

    def train_on_file(self, path: str, sep: str='\t') -> object:
        '''
        The same as self.train, but loads triples from a file instead of having them passed as an argument.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate columns in the file

        :return: the Miaseg model object
        '''
        triples = self.load_train(path, sep=sep)
        return self.train(triples)
    
    def load_train(self, path: str, sep: str='\t') -> set:
        '''
        Loads (root, word, feats) triples from a file.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate columns in the file

        :return: the set of loaded triples
        '''
        triples = set()
        with open(path, 'r') as f:
            for line in f:
                root, word, feats = line.strip().split(sep)
                triples.add((root, word, feats))
        return triples
    
    def train(self, triples: Iterable[tuple[Hashable, Union[str, SegStr], Union[set, tuple]]]) -> object:
        '''
        Trains the Miaseg model on an iterable of (root, word, feats) triples

        :triples: an iterable of (root, word, feats) triples
            - Each :root: should be a unique Hashable identifier
            - Each :word: should be a str or SegStr object
            - Each :feats: should a set or tuple of features marked in the word
            - The model only considers unique triples
        
        :return: the Miaseg model object
        '''

        # TODO

        return self