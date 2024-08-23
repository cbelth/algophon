from typing import Union, Iterable
from abc import abstractmethod

from algophon import SegStr

class Rule:
    def __str__(self) -> str:
        raise NotImplementedError(f'Method __str__ not implemented for {self} of type {type(self)}')

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
        '''
        :pairs: an iterable of (UR, SR) pairs to compute accuracy for
            - Computed over unique pairs

        :return: the accuracy of the rule's predictions of the :pairs:
        '''
        n, m = self.tsp_stats(pairs=pairs)
        return m / n if n > 0 else 0.0

    def tsp_stats(self, pairs: Iterable) -> tuple[int, int]:
        '''
        Computes n and m for the TSP w.r.t a set of pairs

        :pairs: an iterable of (UR, SR) pairs to compute the TSP stats for
            - Computed over unique pairs
        
        :return: n and m
        '''
        n, m = 0, 0
        for ur, sr in set(pairs):
            if isinstance(ur, str):
                ur = SegStr(ur, seginv=self.seginv)
            if isinstance(sr, str):
                sr = SegStr(sr, seginv=self.seginv)
            for idx, pred_sr_seg in self._predictions(ur):
                n += 1
                if sr[idx] == pred_sr_seg:
                    m += 1
        return n, m
    
    @abstractmethod
    def _predictions(self, segstr: SegStr) -> list:
        '''
        :segstr: a SegStr to apply the rule to

        :return: a list of the predictions that the rule makes over :segstr:
            - Each item in the list is a tuple (index, new_seg) specifying each new_seg value predicted and at what index
        '''
        raise NotImplementedError(f'Method _predictions not implemented for {self} of type {type(self)}')