from typing import Union, Iterable

from collections import defaultdict

from algophon import SegInv, SegStr, NatClass
from algophon.symbols import UNDERSPECIFIED, BOUNDARIES
from algophon.models.D2L import Discrepancy, D2LRule, Tier
from algophon.utils import tsp

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

    def __init__(self, 
                 ipa_file_path: Union[None, str]=None, 
                 sep: str='\t') -> object:
        '''
        :ipa_file_path: (Optional; default None) if a str path is passed, the features are used from there
            - Default of None uses Panphon (https://github.com/dmort27/panphon) features
        :sep: (Optional; default '\t') the char separating columns in :ipa_file_path:
            - Only used if :ipa_file_path: is also passed
        '''
        self.seginv = SegInv(add_boundary_symbols=True, ipa_file_path=ipa_file_path, sep=sep)

        self._discrepancy = None # the discrepancy to account for
        self.rule = None

    def __str__(self) -> str:
        if self.rule is None:
            return 'D2L model with no learned rule'
        else:
            return f'D2L model with rule {self.rule}'
    
    def __repr__(self) -> str:
        return self.__str__()

    def train_on_file(self, path: str, sep: str='\t') -> object:
        '''
        The same as self.train, but loads (UR, SR) pairs from a file instead of having them passed as an argument.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate URs from SRs in the file

        :return: the D2L model object
        '''
        pairs = self.load_train(path, sep=sep)
        return self.train(pairs)
    
    def load_train(self, path: str, sep: str='\t') -> set:
        '''
        Loads (UR, SR) pairs from a file.

        :path: the location of the training file
        :sep: (Optional; default '\t') the character used to separate URs from SRs in the file

        :return: the set of loaded (UR, SR) pairs
        '''
        pairs = set()
        with open(path, 'r') as f:
            for line in f:
                ur, sr = line.strip().split(sep)
                pairs.add((ur, sr))
        return pairs

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

        harmony_rule = self.build_rule(pairs=pairs)
        disharmony_rule = self.build_rule(pairs=pairs, harmony=False)
        if harmony_rule and not disharmony_rule: # if only harmony built a productive rule, use it
            self.rule = harmony_rule
        elif disharmony_rule and not harmony_rule: # if only disharmony built a productive rule, use it
            self.rule = disharmony_rule
        elif harmony_rule and disharmony_rule: # if both harmony and disharmony yield a rule, choose the more accurate
            assim_acc, dissim_acc = harmony_rule.accuracy(pairs), disharmony_rule.accuracy(pairs)
            self.rule = harmony_rule if assim_acc >= dissim_acc else disharmony_rule
        else: # neither harmony nor disharmony built a productive rule
            self.rule = None
            self.default = None

        return self # return trained object

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

    # calling a D2L object amounts to calling its produce() method
    __call__ = produce

    def accuracy(self, pairs: Iterable) -> float:
        '''
        :pairs: an iterable of (UR, SR) pairs to compute the TSP stats for
            - Computed over unique pairs

        :return: the accuracy of the rule's predictions of the :pairs:
        '''
        n, c = 0, 0
        for ur, sr in set(pairs):
            pred = self.produce(ur)
            n += 1
            if pred == sr:
                c += 1
        return c / n

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
                    feat_diff = self.seginv.feature_diff(ur_seg, sr_seg) # compute feature diff
                    if self._discrepancy is None: # init discrepancy if it does not exist
                        self._discrepancy = Discrepancy(feat_diff)
                    # tabulate this pair's contribution to the discrepancy
                    self._discrepancy.tabulate(ur=ur, ur_seg=ur_seg, sr_seg=sr_seg)

        return setup_pairs
    
    def build_rule(self, pairs: set, delset: set=set(), tier=None, harmony: bool=True, discrepancy: Union[None, Discrepancy]=None) -> D2LRule:
        '''
        Builds a rule recursively.

        :pairs: a set of (UR, SR) pairs
        :delset: (Optional; default set()) the segments to delete
            - Updated recursively
        :harmony: (Optional; default True) if True, builds a Haromny rule; if False, builds a Disharmony rule
        :discrepancy: (Optional; default None) allows for providing a Discrepancy object
            - Useful for running D2L multiple times for different discrepancies (e.g., as in PLP)
        '''
        if discrepancy is None: # use self._discrepancy by default
            discrepancy = self._discrepancy
        target = discrepancy.get_alternating_UR_segs() # compute target segs

        lctxts, rctxts = self._get_tier_adj_contexts(discrepancy=discrepancy, tier=tier) # compute ctxts
        # build left rule
        left_rule = D2LRule(seginv=self.seginv, target=target, features=discrepancy.feature_diff, left_ctxts=lctxts, tier=tier, harmony=harmony)
        left_underextensions = left_rule.underextension_SRs(pairs=pairs)
        if len(left_underextensions) > 0:
            left_default_sr = sorted(left_underextensions.items(), reverse=True, key=lambda it: it[-1])[0][0]
            left_rule.set_defaults(dict((feat, left_default_sr.features[feat]) for feat in discrepancy.feature_diff))
        # build right rule
        right_rule = D2LRule(seginv=self.seginv, target=target, features=discrepancy.feature_diff, right_ctxts=rctxts, tier=tier, harmony=harmony)
        right_underextensions = right_rule.underextension_SRs(pairs=pairs)
        if len(right_underextensions) > 0:
            right_default_sr = sorted(right_underextensions.items(), reverse=True, key=lambda it: it[-1])[0][0]
            right_rule.set_defaults(dict((feat, right_default_sr.features[feat]) for feat in discrepancy.feature_diff))

        rule = left_rule if left_rule.accuracy(pairs=pairs) >= right_rule.accuracy(pairs=pairs) else right_rule
        n, m = rule.tsp_stats(pairs=pairs)
        if tsp(n=n, m=m):
            ctxt = set(rule.left_ctxts if rule.left_ctxts is not None else rule.right_ctxts)
            if rule.tier is not None: # set the ctxt to the tier if doing so does not change accuracy
                acc_before = rule.accuracy(pairs)
                rule.set_ctxts(ctxts=rule.tier._tierset)
                acc_after = rule.accuracy(pairs)
                if acc_after < acc_before: # change it back
                    rule.set_ctxts(ctxt)
            return rule
        
        # rule not productive

        _old_delset = set(delset)
        delset = delset.union(left_rule.errant_ctxts(pairs).union(right_rule.errant_ctxts(pairs))).difference(target)
        opts = list(NatClass(feats={feat}, seginv=self.seginv) for feat in self.seginv.feature_intersection(delset))
        # filter nat classes that do remove target segs
        opts = list(opt for opt in opts if not any(ur in opt for ur in target))
        if len(opts) > 0:
            best = sorted(opts, key=lambda opt: (len(self.seginv.extension(opt)), f'{opt}'))[0]
            _negate_val = {'+': '-', '-': '+'}
            complement = NatClass(feats=set(f'{_negate_val[feat[0]]}{feat[1:]}' for feat in best.feats), seginv=self.seginv)
            # if the neg of the delset nat class is the the extension complement (e.g., [+syl] vs. [-syl]), use it
            if best.extension_complement().difference(BOUNDARIES) == complement.extension():
                tier = Tier(seginv=self.seginv, feats=complement)
            else: # otherwise, use the delset nat class
                tier = Tier(seginv=self.seginv, feats=best, as_delset=True)
        else:
            complement = self.seginv.segs.difference(delset)
            tier = Tier(seginv=self.seginv, segs=complement)

        if _old_delset == delset: # prevent infinite recursion
            return None
        
        return self.build_rule(pairs=pairs, delset=delset, tier=tier, harmony=harmony, discrepancy=discrepancy)

    def _get_tier_adj_contexts(self, discrepancy: Discrepancy, tier: Union[None, Tier]) -> tuple[set, set]:
        '''
        :discrepancy: a Discrepancy object, which stores the alternating URs
        :tier: a Tier object (if None, will compute adj contexts over input representation)

        :return: the left and right contexts :tier:-adjacent to the target (alternating) segments in the :pairs:
        '''
        URs = discrepancy.get_URs() # compute the alteranting URs
        target = discrepancy.get_alternating_UR_segs() # compute the target (alternating) segments
        left_ctxts, right_ctxts = set(), set() # init ctxt sets
        for ur in URs: # iterate over URs
            projected = tier.project(ur) if tier is not None else ur # project the tier (if there is one)
            for i, seg in enumerate(projected):
                if seg in target: # check if the seg is an alternating (target) seg
                    # compute left context
                    if i > 0:
                        left_ctxts.add(projected[i - 1])
                    # compute right context
                    if i < len(projected) - 1:
                        right_ctxts.add(projected[i + 1])
        return left_ctxts, right_ctxts