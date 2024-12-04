from typing import Union

from algophon import SegStr, NatClass
from algophon.models import Rule

class PLPRule(Rule):
    '''
    Implements an SPE-style rule A -> B / C __ D
    '''

    def __init__(self,
                 seginv,
                 target: set,
                 left_ctxt: Union[None, list[Union[set, NatClass]]]=None,
                 right_ctxt: Union[None, list[Union[set, NatClass]]]=None) -> object:
        '''
        :seginv: a SegInv object
        :target: a set of target (alternating) segments
        :left_ctxts: (optional; default None) left ctxt that triggers rule application: / C __
            - a list of items, each being a set or NatClass object
            - distance from :target: interpreted right to left: / [C_0, C_1, ...] __
        :right_ctxts: (optional; default None) right ctxt that triggers rule application: / __ D
            - a list of items, each being a set or NatClass object
            - distance from :target: interpreted left to right: / __ [D_0, D_1, ...]
        '''
        # init variables
        self.seginv = seginv
        self.target = target
        self.left_ctxt = left_ctxt
        self.right_ctxt = right_ctxt

        # TODO

    def _predictions(self, segstr: SegStr) -> list:
        '''
        :segstr: a SegStr to apply the rule to

        :return: a list of the predictions that the rule makes over :segstr:
            - Each item in the list is a tuple (index, new_seg) specifying each new_seg value predicted and at what index
        '''
        pass
        # TODO

    def __str__(self) -> str:
        pass
        # TODO