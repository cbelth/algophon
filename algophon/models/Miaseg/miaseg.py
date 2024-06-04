from typing import Iterable, Union

from collections import defaultdict, Counter

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
        self._trained = False # model not trained initially (so cannot segment)

    def __str__(self) -> str:
        return 'Mɪᴀꜱᴇɢ'
    
    def __repr__(self) -> str:
        return self.__str__()

    def train_on_file(self, path: str, sep: str='\t', feature_sep: str=';') -> object:
        '''
        The same as self.train, but loads triples from a file instead of having them passed as an argument.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate columns in the file
        :feature_sep: (Optional; default ';') the character used to separate features in the file

        :return: the Miaseg model object
        '''
        triples = self.load_train(path, sep=sep, feature_sep=feature_sep)
        return self.train(triples)
    
    def load_train(self, path: str, sep: str='\t', feature_sep: str=';') -> set:
        '''
        Loads (root, word, feats) triples from a file.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate columns in the file
        :feature_sep: (Optional; default ';') the character used to separate features in the file

        :return: the set of loaded triples
        '''
        triples = list()
        with open(path, 'r') as f:
            for line in f:
                root, word, feats = line.strip('\n').split(sep)
                feats = tuple(feats.split(feature_sep)) if len(feats) > 0 else ()
                triples.append((root, word, feats))
        return triples
    
    def train(self, train: Iterable[tuple[str, Union[str, SegStr], Union[set, tuple]]]) -> object:
        '''
        Trains the Miaseg model on an iterable of (root, word, features) triples

        :train: an Iterable of (root, word, feats) triples
            - Each :root: should be a unique str identifier
            - Each :word: should be a str or SegStr object
            - Each :features: should be a set or tuple of features marked in the word
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
        self._trained = True
        return self
    
    def train_and_segment_file(self, path: str, sep: str='\t', feature_sep: str=';', with_analysis: bool=True) -> list:
        '''
        The same as self.train_and_segment, but loads triples from a file instead of having them passed as an argument.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate columns in the file
        :feature_sep: (Optional; default ';') the character used to separate features in the file
        :with_analysis: (Optiona; default True) if True, returns a morphological analysis (gloss) with each segmentation

         :return: a list of tuples, each containing
            - the triple (index 0)
            - the segmentation of the word (index 1)
            - (if "with_nalysis=True") the morphological analysis/gloss of the word (index 2)
        '''
        triples = self.load_train(path, sep=sep, feature_sep=feature_sep)
        return self.train_and_segment(train=triples, with_analysis=with_analysis)
    
    def train_and_segment(self, train: Iterable[tuple[str, Union[str, SegStr], Union[set, tuple]]], with_analysis: bool=True) -> list:
        '''
        The same as train(), but also segments the training data.

        :train: an Iterable of (root, word, feats) triples
            - Each :root: should be a unique str identifier
            - Each :word: should be a str or SegStr object
            - Each :features: should be a set or tuple of features marked in the word
            - The model only considers unique triples
        :with_analysis: (Optiona; default True) if True, returns a morphological analysis (gloss) with each segmentation
        
        :return: a list of tuples, each containing
            - the triple (index 0)
            - the segmentation of the word (index 1)
            - (if "with_nalysis=True") the morphological analysis/gloss of the word (index 2)
        '''
        self.train(train=train) # train the model
        results = list() # tabluate results
        for triple in train: # segment each triple
            _, word, features = triple
            seg, *ana = self.segment(word=word, features=features, with_analysis=with_analysis)
            bundle = (triple, seg, ana[0]) if with_analysis else (triple, seg) # bundle the results
            results.append(bundle)
        return results
    
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
        types = defaultdict(lambda: defaultdict(int)) # track the inferred types of marked featres (SUFFIX, PREFIX)
        for par in self._paradigms.values(): # iterate over paradigms
            for diff in par.get_one_diff_pairs():
                affix, typ = self._get_marking_from_one_off(src=diff['src'], tgt=diff['tgt'])
                if affix is not None and typ is not None: # if a marking found, tabulate it
                    self.allomorphs[diff['feat']][affix] += 1
                    types[diff['feat']][typ] += 1
                    if typ == SUFFIX:
                        # every feature of src probably comes before the suffix marking the diff
                        for other_feature in diff['shared_feats']:
                            orderings[(other_feature, diff['feat'])] += 1 # other_feature -> diff_feat
                    else: # PREFIX
                        # every feture of src probbly comes after the prefix marking the diff
                        for other_feature in diff['shared_feats']:
                            orderings[(diff['feat'], other_feature)] += 1 # diff_feat -> other_feature
        # retain only the most frequent type of each feature
        self.types = dict((feat, sorted(_typs.items(), reverse=True, key=lambda it: it[-1])[0][0]) for feat, _typs in types.items())
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
    
    def segment(self, word: Union[str, SegStr], features: Union[tuple, set], with_analysis: bool=True) -> Union[list, tuple[list, list]]:
        '''
        Segment a word given the features marked in it.

        :word: should be a str or SegStr object
            - SegStr should only be passed if the parameter use_ipa was True when creating the Miaseg object
        :features: should be a set or tuple of features marked in the word
        :with_analysis: (Optiona; default True) if True, returns a morphological analysis (gloss) with the segmentation

        :return:
            - tuple containing a list of morpheme forms and a list of morpheme meanings (gloss) if :with_analysis: == True
            - list of morpheme forms if :with_analysis: == False
            - If any :features: are have not been attested during training, returns ([:word:], ['FAILED']) if :with_analysis: == True or [:word:]
        '''
        if not self._trained:
            raise ValueError(f'{self} must be trained in order to segment.') 
        if self.use_ipa and isinstance(word, str): # convert str to SegStr if we are using IPA
            word = SegStr(word, seginv=self.seginv)
        elif not self.use_ipa and isinstance(word, SegStr):
            raise ValueError(f'Cannot segment SegStr because {self} object was not constructed with "use_ipa = True"')
        if any(feat not in self.allomorphs for feat in features):
            return ([word], ['FAILED']) if with_analysis else [word]

        # compute prfxs and sufxs        
        prfxs, sufxs = self._get_affixes(features=set(features))
        # create a new object that we can edit without changing :word:
        temp = str(word) if isinstance(word, str) else SegStr(segs=list(word._segs), seginv=self.seginv)

        # init prfx and sufx forms
        prfx_forms = list()
        sufx_forms = list()

        # iterate over prfxs left-to-right
        for prfx in prfxs:
            cand_forms = list(self.allomorphs[prfx].keys())
            matches = list(cand for cand in cand_forms if temp.startswith(cand))
            if len(matches) > 0:
                # choose longest match (breaking ties by frequency)
                best_match = sorted(matches, reverse=True, key=lambda cand: (len(cand), self.allomorphs[prfx][cand]))[0]
            else: # if no matches, match most frequent length of attested forms
                most_freq_len = Counter(list(len(cand) for cand in cand_forms)).most_common(1)[0][0]
                best_match = temp[:most_freq_len]
            temp = temp[len(best_match):]
            prfx_forms.append(best_match)
        # iterate over sufxs right-to-left
        for sufx in reversed(sufxs):
            cand_forms = list(self.allomorphs[sufx].keys())
            matches = list(cand for cand in cand_forms if temp.endswith(cand))
            if len(matches) > 0:
                # choose longest match (breaking ties by frequency)
                best_match = sorted(matches, reverse=True, key=lambda cand: (len(cand), self.allomorphs[sufx][cand]))[0]
            else: # if no matches, match most frequent length of attested forms
                most_freq_len = Counter(list(len(cand) for cand in cand_forms)).most_common(1)[0][0]
                best_match = temp[-most_freq_len:]
            temp = temp[:-len(best_match)]
            sufx_forms.insert(0, best_match)

        # compute segmentation and analysis
        ana = prfxs + ['ROOT'] + sufxs
        seg = prfx_forms + [temp] + sufx_forms

        return (seg, ana) if with_analysis else seg
    
    # calling a Miaseg object amounts to calling its segment() method
    __call__ = segment

    def _get_affixes(self, features: set) -> tuple[list, list]:
        '''
        :features: should be a set or tuple of features marked in the word

        :return: a tuple containing a list of prfxs and a list of sufxs
        '''
        prfxs = list()
        sufxs = list()
        for feature in sorted(features, key=lambda feat: self.order.index(feat)):
            if self.types[feature] == PREFIX:
                prfxs.append(feature)
            else:
                sufxs.append(feature)
        return prfxs, sufxs