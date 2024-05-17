from typing import Iterable, Union

from algophon import Seg, SegInv, NatClass, SegStr
from algophon.symbols import FUNCTION_COMPOSITION, LWB, RWB, UNK
from algophon.models.D2L import Tier

class Rule:
    def __init__(self, 
                 seginv: SegInv,
                 target: set,
                 features: set,
                 left_ctxts: Union[None, set, NatClass]=None, 
                 right_ctxts: Union[None, set, NatClass]=None,
                 tier: Union[None, Tier]=None,
                 harmony: bool=True) -> object:
        '''
        :seginv: a SegInv object
        :target: a set of target (alternating) segments
        :features: a set of features that alternate
        :left_ctxts: (optional; default None) a set of right-adj (to target) segments that trigger rule application
            - Can be a set of specific segments or a NatClass object
        :right_ctxts: (optional; default None) a set of left-adj (to target) segments that trigger a rule application
            - Can be a set of specific segments or a NatClass object
        :tier: (optional; default None) a Tier object to apply the rule over
        :harmony: (optional; default True) specified whether rule enforces harmony or disharmony
        
        Exactly one of :left_ctxts: and :right_ctxts: must be provided.
        '''
        # check arguments
        if left_ctxts is not None and right_ctxts is not None:
            raise ValueError('D2L Rule cannot have both left and right contexts.')
        if left_ctxts is None and right_ctxts is None:
            raise ValueError('D2L Rule must have either left or right contexts.')
        # init variables
        self.seginv = seginv
        self.target = target
        self.features = features
        self.left_ctxts = left_ctxts
        self.right_ctxts = right_ctxts
        self.left_to_right = self.left_ctxts is not None # compute whether rule applies left-to-right or right-to-left
        self.tier = tier
        self.harmony = harmony

    def __str__(self) -> str:
        feat_str = '{' + ','.join(sorted(self.features)) + '}'
        adj_str = f'Agree({self.target},{feat_str})' if self.harmony else f'Disagree({self.target},{feat_str})'
        tier_str = f' {FUNCTION_COMPOSITION} proj({self.tier})' if self.tier is not None else ''
        if self.left_to_right:
            return f'{adj_str} / {self.left_ctxts} __{tier_str}'
        else:
            return f'{adj_str} / __ {self.right_ctxts}{tier_str}'

    def __repr__(self) -> str:
        return self.__str__()
    
    def produce(self, ur: Union[str, SegStr]) -> SegStr:
        '''
        Produces a SR for and input UR

        :ur: the UR to produce an SR for. Can be:
            - space-separated str of IPA symbols
            - SegStr object
        
        :return: a SegStr representing the predicted SR
        '''
        if isinstance(ur, str): # convert str ur to SegStr
            ur = SegStr(ur, seginv=self.seginv)
        new_segs = list(ur._segs) # init new seg list
        # apply predictions
        for idx, seg in self._predictions(segstr=ur):
            new_segs[idx] = seg
        return SegStr(segs=new_segs, seginv=self.seginv) # return SegStr object

    # calling a Rule object amounts to calling its produce() method
    __call__ = produce
    
    def accuracy(self, pairs: Iterable) -> float:
        # TODO
        pass

    def _predictions(self, segstr: SegStr) -> list:
        '''
        :segstr: a SegStr to apply the rule to

        :return: a list of the predictions that the rule makes over :segstr:
            - Each item in the list is a tuple (index, new_seg) specifying each new_seg value predicted and at what index
        '''
        preds = list() # to store predictions
        projection = self.tier.project(segstr=segstr) if self.tier is not None else segstr
        tier_ptr = 0 if self.left_to_right else len(projection) - 1 # init a tier pointer
        while 0 <= tier_ptr <= len(projection) - 1:
            seg = projection[tier_ptr]
            if seg in self.target:
                if self.left_to_right: # left ctxt case
                    ctxt = projection[tier_ptr - 1] if tier_ptr > 0 else LWB
                    if ctxt in self.left_ctxts: # rule applies
                        new_seg = self._apply(seg=seg, ctxt=ctxt)
                        preds.append((projection.idxs[tier_ptr], new_seg))
                        projection._segs[tier_ptr] = new_seg # update tier (iterative application)
                    else: # rule does not apply; use default
                        pass # TODO
                else: # right ctxt case
                    ctxt = projection[tier_ptr + 1] if tier_ptr < len(projection) - 1 else RWB
                    if ctxt in self.right_ctxts: # rule applies
                        new_seg = self._apply(seg=seg, ctxt=ctxt)
                        preds.append((projection.idxs[tier_ptr], new_seg))
                        projection._segs[tier_ptr] = new_seg # update tier (iterative application)
                    else: # rule does not apply; use default
                        pass # TODO
            tier_ptr += 1 if self.left_to_right else -1 # move tier pointer
        return preds
    
    def _apply(self, seg: Seg, ctxt: Seg) -> Seg:
        '''
        :seg: a Seg to (dis)harmonize
        :ctxt: a Seg to (dis)harmoinze to/from

        :return: a Seg like :seg:, but with self.features (dis)harmonized to :ctxt:'s values
        '''
        if self.harmony:
            features = dict((feat, val if feat not in self.features else ctxt.features[feat]) for feat, val in seg.features.items())
        else:
            rev_val = {'+': '-', '-': '+'}
            features = dict((feat, val if feat not in self.features else rev_val[ctxt.features[feat]]) for feat, val in seg.features.items())
        # compute vec_to_seg dict
        vec_to_seg = dict((','.join(list(f'{val}{feat}' for feat, val in _seg.features.items())), _seg) for _seg in self.seginv.segs)
        # compute vec
        vec = ','.join(list(f'{val}{feat}' for feat, val in features.items()))
        return vec_to_seg[vec] if vec in vec_to_seg else seg
