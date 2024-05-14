from typing import Union

from algophon import Seg, NatClass, SegInv

class Tier:
    def __init__(self, seginv: SegInv, feats: Union[NatClass, set, None]=None, segs: Union[set, None]=None) -> object:
        '''
        :feats: (Optional) a feature-specification of the tier. One of the following
            - NatClass object
            - set of features; will be automatically convereted to a NatClass object
            - None; :segs: must be passed instead to define the Tier
        :seginv: a SegInv object
        :segs: (Optional) a set of particular segments. Will automatically be converted to Seg objects if currently str objects.
            - None; :feats: must be passed instead to define the Tier

        Exactly one of :feats: and :segs: must be provided (no more no less) to define the Tier.
        '''
        if feats is not None and segs is not None:
            raise ValueError(f'Arguments :feats: and :segs: both provided. Only pass one.')
        if not feats and not segs:
            raise ValueError(f'Either :feats: or :segs: must be passed to define the tier, but neither was passed.')
        
        self.seginv = seginv # init self.seginv

        if segs is not None: # a set of Segs
            self._tierset = set(self.seginv.add_and_get(seg) for seg in segs)
        elif isinstance(feats, NatClass): # a NatClass object
            self._tierset = feats
        elif isinstance(feats, set): # a set of features
            self._tierset = NatClass(feats=feats, seginv=self.seginv)

        # init self._str
        self._str = self._tierset.__str__() if not isinstance(self._tierset, set) else '{' + f'{",".join(sorted(list(f"{seg}" for seg in self._tierset)))}' + '}'

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return self.__str__()
    
    def __contains__(self, key: Union[str, Seg]) -> bool:
        return key in self._tierset