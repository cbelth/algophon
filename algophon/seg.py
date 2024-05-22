class Seg:
    '''
    A class representing a phonological segment.

    Allows for an ipa symbol to represent the segment as shorthand, but treats the segment as a feature bundle internally.
    '''
    def __init__(self, ipa: str, features: dict=dict()):
        self._ipa = ipa
        self.features = features

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