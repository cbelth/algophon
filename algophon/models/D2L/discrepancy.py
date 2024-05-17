from algophon import Seg, SegStr

class Discrepancy:
    '''
    A class for representing a discrepancy—i.e., a difference between URs and SRs.
    '''

    def __init__(self, feature_diff) -> object:
        '''
        '''
        self.alternations = set()
        self.annotated = list()
        self.feature_diff = feature_diff

    def __contains__(self, item):
        return item in self.alternations

    def __str__(self):
        return self.feature_diff.__str__()

    def __repr__(self):
        return self.__str__()

    def tabulate(self, ur: SegStr, i: int, ur_seg: Seg, sr_seg: Seg) -> None:
        '''
        '''
        self.annotated.append((ur, i, sr_seg))
        self.alternations.add((ur_seg, sr_seg))

    def get_alternating(self):
        return set(it[0] for it in self.alternations).union(it[1] for it in self.alternations)

    def get_alternating_urs(self):
        return set(it[0] for it in self.alternations)