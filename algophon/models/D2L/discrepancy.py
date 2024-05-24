from algophon import Seg, SegStr

class Discrepancy:
    '''
    A class for representing a discrepancy—i.e., a difference between URs and SRs.
    '''

    def __init__(self, feature_diff: set) -> object:
        '''
        :feature_diff: the features that differ between alternating ur_seg ~ sr_seg pairs
        '''
        self.alternations = set() # stores the (ur_seg ~ sr_seg) alternations corresponding to the discrepancy
        self.instances = set() # stores each instance of the discrepancy
        self.feature_diff = feature_diff

    def __contains__(self, item: tuple) -> bool:
        return item in self.alternations

    def __str__(self) -> str:
        return self.feature_diff.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def tabulate(self, ur: SegStr, i: int, ur_seg: Seg, sr_seg: Seg) -> None:
        '''
        :ur: the UR exibiting the discrepancy
        :i: the index where the discrepancy occurs
        :ur_seg:, :sr_seg: the ur_seg ~ sr_seg alternation

        :return: None
        '''
        self.alternations.add((ur_seg, sr_seg)) # update alternations
        self.instances.add((ur, i, sr_seg)) # update instances

    def get_alternating(self) -> set:
        '''
        :return: a set of all the underling and surface Seg objects that are involved in the alternation
        '''
        return set(it[0] for it in self.alternations).union(it[1] for it in self.alternations)

    def get_alternating_UR_segs(self) -> set:
        '''
        :return: a set of all the underling Seg objects that are involved in the alternation
        '''
        return set(it[0] for it in self.alternations)
    
    def get_URs(self) -> set:
        '''
        :return: a set of all the URs that are involved in the alternation
        '''
        return set(it[0] for it in self.instances)