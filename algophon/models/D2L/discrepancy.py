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
        self.URs = set() # stores each UR with a discrepancy
        self.feature_diff = feature_diff

    def tabulate(self, ur: SegStr, ur_seg: Seg, sr_seg: Seg) -> None:
        '''
        :ur: the UR exibiting the discrepancy
        :ur_seg:, :sr_seg: the ur_seg ~ sr_seg alternation

        :return: None
        '''
        self.alternations.add((ur_seg, sr_seg)) # update alternations
        self.URs.add(ur) # update URs set

    def get_alternating_UR_segs(self) -> set:
        '''
        :return: a set of all the underling Seg objects that are involved in the alternation
        '''
        return set(it[0] for it in self.alternations)
    
    def get_URs(self) -> set:
        '''
        :return: the set of all URs that are involved in the alternation
        '''
        return self.URs