from typing import Iterable, Union

from algophon import SegInv, NatClass

class Rule:
    def __init__(self, 
                 seginv: SegInv,
                 target: set,
                 left_ctxts: Union[None, set, NatClass]=None, 
                 right_ctxts: Union[None, set, NatClass]=None,
                 harmony=True) -> object:
        '''
        :seginv: a SegInv object
        :target: a set of target (alternating) segments
        :left_ctxts: (optional) a set of right-adj (to target) segments that trigger rule application
            - Can be a set of specific segments or a NatClass object
        :right_ctxts: (optional) a set of left-adj (to target) segments that trigger a rule application
            - Can be a set of specific segments or a NatClass object
        
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
        self.left_ctxts = left_ctxts
        self.right_ctxts = right_ctxts
        self.left_to_right = self.left_ctxts is not None
        self.harmony = harmony

    def __repr__(self) -> str:
        return self.__str__()
    
    def accuracy(self, pairs: Iterable) -> float:
        # TODO
        pass