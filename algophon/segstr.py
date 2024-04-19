class SegStr:
    '''
    A class representing a sequence of phonological segments (Seg objects).
    '''
    def __init__(self, segs, seginv):
        '''
        :segs: Can be any of the following:
            - a str of IPA symbols, where each symbol is separated by a space ' '
            - a list of IPA symbols
            - a list of Seg objects
        :seginv: a SegInv object
        '''
        self._seginv = seginv

        if isinstance(segs, list):
            self._segs = list(self._seginv.add_and_get(seg) for seg in segs)
        elif isinstance(segs, str):
            self._segs = list(self._seginv.add_and_get(seg) for seg in segs.split())
        else:
            raise ValueError(f':segs: should be a list of IPA symbols, a list of Seg objects, or a str of space-separated IPA symbols, instead found type {type(segs)}')
        
        # compute str form
        self._str = ''
        for seg in self._segs:
            self._str += f'{seg}'
        
    def __len__(self) -> int:
        return len(self._segs)
    
    def __str__(self) -> str:
        return self._str
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        '''
        Uses hash of space-separated IPA symbols
        '''
        return hash(' '.join(f'{seg}' for seg in self._segs))
    
    def __eq__(self, other: object) -> bool:
        '''
        :other: Can be any of the following:
            - a str of IPA symbols, where each symbol is separated by a space ' '
            - a list of IPA symbols
            - a list of Seg objects
            - a SegStr object
        '''
        if isinstance(other, str): # works for lists of IPA symbols and of Seg objects b.c. Seg objects implement __eq__ based on their IPA symbol
            return self._segs == other.split()
        elif isinstance(other, list): # works for lists of IPA symbols and of Seg objects b.c. Seg objects implement __eq__ based on their IPA symbol
            return self._segs == other
        elif isinstance(other, SegStr):
            return self._segs == other._segs
        else:
            raise ValueError(f'Cannot compare a SegStr object with an object of type {type(other)}')
        
    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __lt__(self, other) -> bool:
        '''
        :other: a SegStr object
        '''
        if not isinstance(other, SegStr):
            raise ValueError(f'Cannot compare a SegStr object with an object of type {type(other)}')
        return self._segs() < other._segs()
    
    def __getitem__(self, idx):
        '''
        Handles slicing and indexing like a str or list

        :return: 
            - Slicing: SegStr object containing the slice
            - Indexing: Seg object at the index
        '''
        res = self._segs.__getitem__(idx)
        if isinstance(res, list): # handle a slice
            return SegStr(segs=res, seginv=self._seginv)
        return res # handle an index
    
    def __add__(self, other: object):
        '''
        Handles concatenation.

        :other: Can be any of the following:
            - a str of IPA symbols, where each symbol is separated by a space ' '
            - a list of IPA symbols
            - a list of Seg objects
            - a SegStr object

        :return: a new SegStr object containing the concatenation
        '''
        if isinstance(other, str) or isinstance(other, list):
            other = SegStr(other, seginv=self._seginv)
        elif not isinstance(other, SegStr):
            raise ValueError(f'Cannot concatenate a SegStr object with an object of type {type(other)}')
        return SegStr(segs=self._segs + other._segs, seginv=self._seginv)
    
    def __iter__(self):
        '''
        Iterating over a SegStr is the same as iterating over its Seg objects.
        '''
        return self._segs.__iter__()

    '''
    Equivalents of str & list methods
    '''
    
    def startswith(self, other: object) -> bool:
        '''
        :other: Can be any of the following:
            - a str of IPA symbols, where each symbol is separated by a space ' '
            - a list of IPA symbols
            - a list of Seg objects
            - a SegStr object
        '''
        if isinstance(other, str):
            other = other.split()
        elif not isinstance(other, list) and not isinstance(other, SegStr):
            raise ValueError(f'Cannot compare a SegStr object with an object of type {type(other)}')
        for idx in range(len(other)):
            if self._segs[idx] != other[idx]:
                return False
        return True
    
    def endswith(self, other: object) -> bool:
        '''
        :other: Can be any of the following:
            - a str of IPA symbols, where each symbol is separated by a space ' '
            - a list of IPA symbols
            - a list of Seg objects
            - a SegStr object
        '''
        if isinstance(other, str):
            other = other.split()
        elif not isinstance(other, list) and not isinstance(other, SegStr):
            raise ValueError(f'Cannot compare a SegStr object with an object of type {type(other)}')
        idx = -1
        for offset in range(len(other)):
            if self._segs[idx - offset] != other[idx - offset]:
                return False
        return True

    def count(self, item: object) -> int:
        '''
        :item: Can be either of the following:
            - str IPA symbol
            - Seg object

        :return: the number of instances of :item: in :self:
        '''
        return self._segs.count(item)