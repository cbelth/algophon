class SegStr:
    '''
    A class representing a sequence of phonological segments (Seg objects).
    '''
    def __init__(self, segs, seg_inv):
        self._segs = segs
        self._seg_inv = seg_inv