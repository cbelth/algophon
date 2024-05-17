from typing import Union, Iterable

from algophon import SegInv, SegStr
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

    def train(self, pairs: Iterable) -> object:
        '''
        :pairs: a list of (UR, SR pairs)
            - Each UR and SR should be one of the following:
                - space separated str of IPA symbols
                - SegStr object
            - The model only considers unique (UR, SR) pairs, because learning is over types not tokens.
        '''
        pairs = self._train_setup(pairs) # set everything up to train
        # TODO
        return self

    def produce(self, ur: SegStr) -> SegStr:
        '''
        '''
        pass # TODO

    def _train_setup(self, pairs: Iterable) -> set:
        '''
        This method does two things:
            1) Converts :pairs: to a set so that all pairs are unique, and converts URs and SRs to SegStr objects if they are strs.
            2) Builds a Discrepancy object to represent the discrepancy between URs and SRs

        :pairs: a list of (UR, SR pairs)
            - The same as the :pairs: argument for self.train()

        :return: a set of unique (UR, SR) tuples, where each UR and SR is a SegStr object
        '''
        setup_pairs = set() # make the training pairs a set (in case there are any duplicates—learning is over types!)
        for ur, sr in pairs:
            # make ur and sr SegStr objects (if they are not already)
            ur, sr = SegStr(ur, self.seginv) if isinstance(ur, str) else ur, SegStr(sr, self.seginv) if isinstance(sr, str) else sr
            if len(ur) != len(sr):
                raise ValueError(f'D2L currently only handles (dis)harmony, not epenthesis and deletion. \
                                 You passed at least one pair ({ur}, {sr}) of different lengths, namely ({len(ur), len(sr)})')
            setup_pairs.add((ur, sr))

            # figure out what the discrepancy is
            for i in range(len(ur)):
                ur_seg, sr_seg = ur[i], sr[i] # extract segments
                if ur_seg != sr_seg: # update discrepancy
                    feat_diff = tuple(sorted(self.seginv.feature_diff(ur_seg, sr_seg))) # compute feature diff
                    if self._discrepancy is None: # init discrepanchy if it does not exist
                        self._discrepancy = Discrepancy(feat_diff)
                    self._discrepancy.tabulate(ur, i, ur_seg, sr_seg) # tabulate this pair's contribution to the discrepancy
        return setup_pairs

    # calling the D2L object amounts to calling its produce() method
    __call__ = produce