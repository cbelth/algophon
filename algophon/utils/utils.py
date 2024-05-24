import numpy as np

def tsp(n: int, e: int=None, m: int=None) -> bool:
    '''
    Computes whether the Tolerance/Sufficiency Principle (TSP) threshold is satisfied.

    :n: the number of items in the rule's scope
    :e: (optional) the number of exceptions to the rule
        - Must be provided if :m: is not
    :m: (optional) the number of items following the rule (n - e)
        - Must be provided if :e: is not

    If both :e: and :m: are passed, it must be that :m: = :n: - :e:

    :return: True if the threshold is satisfied, False if not
        - Because the TSP is not well-defined for very small n, the functions returns False if m < 2 or m < n / 2
    '''
    if e is None and m is None:
        raise ValueError('Either :e: or :m: must be provided.')
    if e is not None and m is not None and m != n - e:
        raise ValueError(f'Passed both :e: (= {e}) and :m: (= {m}), but they are incompatible: {m} != {n} - {e}')
    if e is None: # compute e from n and m
        e = n - m
    if m is None: # compute m from n and e
        m = n - e
    return m > 1 and m >= n / 2 and e <= n / np.log(n)