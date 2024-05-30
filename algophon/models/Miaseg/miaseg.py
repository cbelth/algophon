from typing import Iterable, Union

from algophon import SegStr, SegInv
from algophon.models.Miaseg import Paradigm

class Miaseg:
    '''
    An implementation of the model "Meaning Informed Segmentation of Agglutinative Morphology" (Mɪᴀꜱᴇɢ) from Belth (2024)

    Belth, Caleb. 2024. Meaning-Informed Low-Resource Segmentation of Agglutinative Morphology. SCiL.
    @inproceedings{belth2024miaseg,
        title={Meaning-Informed Low-Resource Segmentation of Agglutinative Morphology},
        author={Belth, Caleb},
        booktitle={Proceedings of the Society for Computation in Linguistics},
        year={2024}
    }
    '''

    def __init__(self, 
                 use_ipa: bool=False,
                 ipa_file_path: Union[None, str]=None, 
                 sep: str='\t') -> object:
        '''
        :use_ipa: (Optional; default False) if True, interprets words as sequences of IPA symbols
            - if False (default), interprets words as orthography
        :ipa_file_path: (Optional; default None) if a str path is passed, the features are used from there
            - Default of None uses Panphon (https://github.com/dmort27/panphon) features
            - Only used if :orthography: == False
        :sep: (Optional; default '\t') the char separating columns in :ipa_file_path:
            - Only used if :ipa_file_path: is also passed
            - Only used if :orthography: == False
        '''
        self.use_ipa = use_ipa
        if use_ipa: # if we are using IPA, set up a SegInv object
            self.seginv = SegInv(add_boundary_symbols=True, ipa_file_path=ipa_file_path, sep=sep)

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
    
    def train(self, triples: Iterable[tuple[str, Union[str, SegStr], Union[set, tuple]]]) -> object:
        '''
        Trains the Miaseg model on an iterable of (root, word, features) triples

        :triples: an Iterable of (root, word, feats) triples
            - Each :root: should be a unique str identifier
            - Each :word: should be a str or SegStr object
            - Each :features: should a set or tuple of features marked in the word
            - The model only considers unique triples
        
        :return: the Miaseg model object
        '''
        if self.use_ipa: # convert each word to a SegStr if we are using IPA
            triples = list((root, 
                            SegStr(word, seginv=self.seginv) if not isinstance(word, SegStr) else word, 
                            tuple(sorted(feats)))
                                for root, word, feats in triples)
        self._setup_paradigms(triples) # set up paradigms
        # TODO

        return self
    
    def _setup_paradigms(self, train: Iterable) -> None:
        '''
        Sets up the model's paradigms

        :triples: an Iterable of (root, word, feats) triples
        '''
        self._paradigms = dict() # init paradigms object
        for root, word, features in train:
            if root not in self._paradigms: # init this paradigm
                self._paradigms[root] = Paradigm(root=root)
            # add the word to the paradigm
            self._paradigms[root].add_word(word=word, features=features)