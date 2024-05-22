from typing import Union

from algophon import Seg, SegStr, NatClass, SegInv
from algophon.symbols import NEG

class Tier:
    def __init__(self, seginv: SegInv, feats: Union[NatClass, set, None]=None, segs: Union[set, None]=None, as_delset: bool=False) -> object:
        '''
        :feats: (Optional) a feature-specification of the tier. One of the following
            - NatClass object
            - set of features; will be automatically convereted to a NatClass object
            - None; :segs: must be passed instead to define the Tier
        :seginv: a SegInv object
        :segs: (Optional) a set of particular segments. Will automatically be converted to Seg objects if currently str objects.
            - None; :feats: must be passed instead to define the Tier
        :as_delset: (Optional; default False) if True, :feats: is interpreted as a deletion set rather (i.e., containment is attained by *not* being in self._tierset)

        Exactly one of :feats: and :segs: must be provided (no more no less) to define the Tier.
        '''
        if feats is not None and segs is not None:
            raise ValueError(f'Arguments :feats: and :segs: both provided. Only pass one.')
        if not feats and not segs:
            raise ValueError(f'Either :feats: or :segs: must be passed to define the tier, but neither was passed.')
        
        self.seginv = seginv # init self.seginv
        self.as_delset = as_delset

        if segs is not None: # a set of Segs
            self._tierset = set(self.seginv.add_and_get(seg) for seg in segs)
        elif isinstance(feats, NatClass): # a NatClass object
            self._tierset = feats
        elif isinstance(feats, set): # a set of features
            self._tierset = NatClass(feats=feats, seginv=self.seginv)

        # init self._str
        self._str = self._tierset.__str__() if not isinstance(self._tierset, set) else '{' + f'{",".join(sorted(list(f"{seg}" for seg in self._tierset)))}' + '}'
        if self.as_delset:
            self._str = f'{NEG}{self._str}'

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return self.__str__()
    
    def __contains__(self, key: Union[str, Seg]) -> bool:
        if self.as_delset:
            return key not in self._tierset
        return key in self._tierset
    
    def project(self, segstr: SegStr) -> SegStr:
        '''
        :segstr: a SegStr object to project the tier w.r.t

        :return: a Tier.Projection object
            - A sublcass of SegStr that includes a .idxs variable storing the indexes of the projected segments in the original SegStr
        '''
        if not isinstance(segstr, SegStr):
            raise ValueError(f'Tier projection not implemented for segstr of type {type(segstr)}')
        proj, idxs = list(), list()
        for idx, seg in enumerate(segstr):
            if seg in self:
                proj.append(seg)
                idxs.append(idx)
        return Tier.Projection(segs=proj, idxs=idxs, seginv=self.seginv)
    
    class Projection(SegStr):
        def __init__(self, segs, idxs, seginv):
            self.idxs = idxs
            super().__init__(segs=segs, seginv=seginv)