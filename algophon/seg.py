class Seg:
    '''
    A class representing a phonological segment.

    Allows for an ipa symbol to represent the segment as shorthand, but treats the segment as a feature bundle internally.
    '''
    def __init__(self, ipa: str, features: dict=None):
        self._ipa = ipa
        self.features = features if features is not None else dict()

    def __str__(self) -> str:
        return self._ipa
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__str__())
    
    def __eq__(self, other: object) -> bool:
        return self.__hash__() == other.__hash__()
    
    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other: object) -> bool:
        return f'{self}'.__gt__(f'{other}')

    def __ge__(self, other: object) -> bool:
        return f'{self}'.__ge__(f'{other}')

    def __lt__(self, other: object) -> bool:
        return f'{self}'.__lt__(f'{other}')

    def __le__(self, other: object) -> bool:
        return f'{self}'.__le__(f'{other}')
    
    def __len__(self) -> int:
        '''
        Length of a segment is always 1
        '''
        return 1
    
    def __getitem__(self, feature: str) -> str:
        '''
        :feature: a feature, whose value to return

        :return: the value ('+', '-', '0') of the :feature:
        '''
        return self.features.__getitem__(feature)
    
    def __setitem__(self, feature: str, val: str) -> None:
        '''
        :feature: a feature, whose value to set
        :val: a value to set for :feature:

        :return: None
        '''
        if feature not in self.features:
            raise ValueError(f":feature: '{feature}' not in self.features")
        self.features.__setitem__(feature, val)

    def __add__(self, other: object):
        '''
        Handles concatenation.

        :other: Can be any of the following:
            - a SegStr object

        :return: a new SegStr object containing the concatenation
        '''
        from algophon.segstr import SegStr
        if isinstance(other, SegStr):
            return SegStr([self] + other._segs, seginv=other._seginv)
        raise ValueError(f'Cannot concatenate a Seg object with an object of type {type(other)}')
