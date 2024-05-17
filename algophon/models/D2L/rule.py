from typing import Iterable

class Rule:
    def __init__(self, harmony=True) -> object:
        self.harmony = harmony
        # TODO
        pass

    def __repr__(self) -> str:
        return self.__str__()
    
    def accuracy(self, pairs: Iterable) -> float:
        # TODO
        pass