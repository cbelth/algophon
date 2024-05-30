from typing import Iterable, Union

from collections import defaultdict

from algophon import SegStr, SegInv
from algophon.models.Miaseg import Paradigm
from algophon.data_structures import Graph

SUFFIX = 'SUFFIX'
PREFIX = 'PREFIX'

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
    
    def train(self, train: Iterable[tuple[str, Union[str, SegStr], Union[set, tuple]]]) -> object:
        '''
        Trains the Miaseg model on an iterable of (root, word, features) triples

        :train: an Iterable of (root, word, feats) triples
            - Each :root: should be a unique str identifier
            - Each :word: should be a str or SegStr object
            - Each :features: should a set or tuple of features marked in the word
            - The model only considers unique triples
        
        :return: the Miaseg model object
        '''
        if self.use_ipa: # convert each word to a SegStr if we are using IPA
            train = list((root, 
                          SegStr(word, seginv=self.seginv) if not isinstance(word, SegStr) else word, 
                          tuple(sorted(feats)))
                            for root, word, feats in train)
        self._setup_paradigms(train) # set up paradigms
        self._find_allomorphs(train) # find allomorphs
        return self
    
    def _setup_paradigms(self, train: Iterable) -> None:
        '''
        Sets up the model's paradigms

        :train: an Iterable of (root, word, feats) triples
        '''
        self._paradigms = dict() # init paradigms object
        for root, word, features in train:
            if root not in self._paradigms: # init this paradigm
                self._paradigms[root] = Paradigm(root=root)
            # add the word to the paradigm
            self._paradigms[root].add_word(word=word, features=features)

    def _find_allomorphs(self, train: Iterable) -> None:
        '''
        Computes possible allomorphs for each feature, and orders them.

        :train: an Iterable of (root, word, feats) triples
        '''
        orderings = defaultdict(int) # track the inferred pairwise orderings
        self.allomorphs = defaultdict(lambda: defaultdict(int)) # track the inferred allomorphs of marked features
        self.types = defaultdict(lambda: defaultdict(int)) # track the inferred types of marked featres (SUFFIX, PREFIX)
        for par in self._paradigms.values(): # iterate over paradigms
            for diff in par.get_one_diff_pairs():
                affix, typ = self._get_marking_from_one_off(src=diff['src'], tgt=diff['tgt'])
                if affix is not None and typ is not None: # if a marking found, tabulate it
                    self.allomorphs[diff['feat']][affix] += 1
                    self.types[diff['feat']][typ] += 1
                    if typ == SUFFIX:
                        # every feature of src probably comes before the suffix marking the diff
                        for other_feature in diff['shared_feats']:
                            orderings[(other_feature, diff['feat'])] += 1 # other_feature -> diff_feat
                    else: # PREFIX
                        # every feture of src probbly comes after the prefix marking the diff
                        for other_feature in diff['shared_feats']:
                            orderings[(diff['feat'], other_feature)] += 1 # diff_feat -> other_feature

        # remove conflicting x <-> y by choosing the one with higher frequency
        orderings = list((x, y) for x, y in list(orderings.keys()) if orderings[(x, y)] >= orderings[(y, x)])
        # build DAG encoding ordering
        graph = Graph(directed=True)
        graph.add_edges(orderings)
        # topologically sort the graph
        self.order = graph.topological_sort()

    def _get_marking_from_one_off(self, src: Union[str, SegStr], tgt: Union[str,  SegStr]) -> tuple[Union[str, SegStr], str]:
        '''
        :src: a str/SegStr that has fewer marked features
        :tgt: a str/SegStr that has more marked features

        :return: a tuple containing the affix and the affix type
        '''
        if tgt.startswith(src): # feat marked with suffix
            return tgt[len(src):], SUFFIX
        if tgt.endswith(src): # feat marked with prefix
            return tgt[:len(tgt) - len(src)], PREFIX
        return None, None # cannot determine how feature marked