class NatClass:
    def __init__(self, feats, seg_inv):
        self.feats = set(feats)
        self._seg_inv = seg_inv
        self._name = '[' + ','.join(sorted(self.feats)) + ']'

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self.__str__()
    
    def __contains__(self, seg) -> bool:
        '''
        :seg: a str IPA segment or Seg object

        :return: True if the :seg: is in the NatClass, False otherwise
        '''
        seg = self._seg_inv[seg]
        return all(seg.features[feat[1:]] == feat[0] for feat in self.feats)
    
    def extension(self) -> set:
        '''
        :return: the extensional representation of the natural class
        '''
        return self._seg_inv.extension(self)
    
    def extension_complement(self) -> set:
        '''
        :return: the extensional complement of the natural class relative to self._seg_inv: SegInv \ NatClass
        '''
        return self._seg_inv.extension_complement(self)

