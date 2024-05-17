from typing import Union, Iterable

from collections import defaultdict

from algophon import SegInv, SegStr
from algophon.symbols import UNDERSPECIFIED
from algophon.models.D2L import Discrepancy

class D2L:
    '''
    An implementation of the model "Distant to Local" (D2L) from Belth (2024)

    Belth, Caleb. 2024. A Learning-Based Account of Phonological Tiers. Linguistic Inquiry.
    @article{belth2024tiers,
        title={A Learning-Based Account of Phonological Tiers},
        author={Belth, Caleb},
        journal={Linguistic Inquiry},
        year={2024},
        publisher={MIT Press},
        url = {https://doi.org/10.1162/ling\_a\_00530},
    }
    '''

    def __init__(self, seginv: Union[None, SegInv]=None, verbose=True) -> object:
        self.seginv = seginv if seginv is not None else SegInv()
        self.verbose = verbose

        self._discrepancy = None # the discrepancy to account for
        self.rule = None

    def train_on_file(self, path: str, sep: str='\t') -> object:
        '''
        The same as self.train, but loads (UR, SR) pairs from a file instead of having them passed as an argument.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate URs from SRs in the file

        :return: the D2L model object
        '''
        pairs = self._load_train(path, sep=sep)
        return self.train(pairs)

    def train(self, pairs: Iterable) -> object:
        '''
        Trains the D2L model on an iterable of (UR, SR) pairs

        :pairs: an iterable of (UR, SR) pairs
            - Each UR and SR should be one of the following:
                - space separated str of IPA symbols
                - SegStr object
            - The model only considers unique (UR, SR) pairs, because learning is over types not tokens.

        :return: the D2L model object
        '''
        pairs = self._train_setup(pairs) # set everything up to train

        return self

    def produce(self, ur: Union[SegStr, str]) -> SegStr:
        '''
        :ur: a UR in one of the following forms:
            - space separated str of IPA symbols
            - SegStr object
        
        :return: the SR predicted by the model (= :ur: if there is no rule, or the rule does not apply)
        '''
        if isinstance(ur, str): # convert str to SegStr
            ur = SegStr(ur, seginv=self.seginv)

        sr = ur # init sr to equal ur
        if self.rule is not None: # if there is a rule, apply it
            sr = self.rule(sr)
        return sr # return sr

    # calling the D2L object amounts to calling its produce() method
    __call__ = produce

    def _load_train(self, path: str, sep: str) -> set:
        '''
        :path: the same as in self.train_on_file
        :sep: the same as in self.train_on_file

        :return: a set of UR, SR pairs loaded from the file at :path:
        '''
        pairs = set()
        with open(path, 'r') as f:
            for line in f:
                ur, sr = line.strip().spit(sep)
                pairs.add((ur, sr))
        return pairs

    def _train_setup(self, pairs: Iterable) -> set:
        '''
        This method does two things:
            1) Converts :pairs: to a set so that all pairs are unique, and converts URs and SRs to SegStr objects if they are strs.
            2) Builds a Discrepancy object to represent the discrepancy between URs and SRs

        :pairs: a list of (UR, SR pairs)
            - The same as the :pairs: argument for self.train()

        :return: a set of unique (UR, SR) tuples, where each UR and SR is a SegStr object
        '''

        # handle abstract URs
        
        abstract_URs = defaultdict(set)
        for ur, sr in pairs:
            sr = SegStr(sr, self.seginv) if isinstance(sr, str) else sr
            if isinstance(ur, str): # if the UR is already a SegStr, then any abstract URs must have already been added by the user
                ur = ur.split() # split on spaces
                for i in range(len(ur)): # look for discrepancies
                    ur_seg, sr_seg = ur[i], sr[i] # extract segments
                    if ur_seg != sr_seg and ur_seg not in self.seginv._seg_to_feat_vec: # tabulate abstract underlying seg
                        abstract_URs[ur_seg].add(sr_seg)
        
        for ur, srs in abstract_URs.items(): # compute the UR features for each abstract UR
            shared_feats = set(feat[1:] for feat in self.seginv.feature_intersection(srs, exclude_underspecified=False))
            feature_diff = set(self.seginv.feature_space).difference(shared_feats)
            example_sr = list(srs)[0]
            # compute a feature dictionary, where shared features are specified and the unshared features are UNDERSPECIFIED
            features = dict((feat, val if feat not in feature_diff else UNDERSPECIFIED) for feat, val in self.seginv[example_sr].features.items())
            self.seginv.add_custom(symbol=ur, features=features)

        # build pairs and discrepancy

        setup_pairs = set() # make the training pairs a set (in case there are any duplicates—learning is over types!)
        for ur, sr in pairs:
            # make ur and sr SegStr objects (if they are not already)
            sr = SegStr(sr, self.seginv) if isinstance(sr, str) else sr
            ur = SegStr(ur, self.seginv) if isinstance(ur, str) else ur
            if len(ur) != len(sr):
                raise ValueError(f'D2L currently only handles (dis)harmony, not epenthesis and deletion. You passed at least one pair ({ur}, {sr}) of different lengths, namely ({len(ur), len(sr)})')
            setup_pairs.add((ur, sr))

            # figure out what the discrepancy is
            for i in range(len(ur)):
                ur_seg, sr_seg = ur[i], sr[i] # extract segments
                if ur_seg != sr_seg: # update discrepancy
                    feat_diff = tuple(sorted(self.seginv.feature_diff(ur_seg, sr_seg))) # compute feature diff
                    if self._discrepancy is None: # init discrepanchy if it does not exist
                        self._discrepancy = Discrepancy(feat_diff)
                    # tabulate this pair's contribution to the discrepancy
                    self._discrepancy.tabulate(ur=ur, i=i, ur_seg=ur_seg, sr_seg=sr_seg)

        return setup_pairs