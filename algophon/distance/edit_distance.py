import numpy as np
from typing import Union
from algophon import SegStr, SegInv
from algophon.symbols import EMPTY

UP_ARROW = '↑'
LEFT_ARROW = '←'
DIAG_ARROW = '↖'

def _compute_table(s1: SegStr, s2: SegStr) -> np.array:
    '''
    '''
    n = len(s1) # s1 (len n) forms the rows of the table
    m = len(s2) # sw (len m) forms the cols of the table
    # dynamic programming table D, where D(i,j) is the edit distance of s1[1...i] and s2[1...j]
    table = np.empty((n + 1, m + 1), dtype='object')

    # init table
    for i in range(n + 1): # s1 (len n) forms the rows of the table
        for j in range(m + 1): # s2 (len m) forms the cols of the table
            table[i, j] = { # init cell
                'i': i, 
                'j': j, 
                's1_seg': s1[i - 1], 
                's2_seg': s2[j - 1],
                'pointers': list(),
            }
            # init base cases
            if j == 0:
                table[i, 0]['distance'] = i
                if i != 0:
                    table[i, 0]['pointers'].append(UP_ARROW)
            if i == 0:
                table[0, j]['distance'] = j
                if j != 0:
                    table[0, j]['pointers'].append(LEFT_ARROW)
                    
    # recursive case
    for i in range(1, n + 1): # build table one row at a time
        for j in range(1, m + 1): # build row one col at a time
            v1 = table[i - 1, j]['distance'] + 1
            v2 = table[i, j - 1]['distance'] + 1
            v3 = table[i - 1, j - 1]['distance'] + (1 if s1[i - 1] != s2[j - 1] else 0)
            distance = min([v1, v2, v3])
            # set distance
            table[i, j]['distance'] = distance
            # set pointers
            if distance == v1: # move up one row
                table[i, j]['pointers'].append(UP_ARROW)
            if distance == v2: # move left one col
                table[i, j]['pointers'].append(LEFT_ARROW)
            if distance == v3: # move up one row and left one col
                table[i, j]['pointers'].append(DIAG_ARROW)

    return table

def _get_paths(cell: dict, table: np.array) -> tuple[list, list]:
    '''
    Recursively computes all paths from the :cell: to the (0, 0) cell, along with the corresponding alignments.
    '''
    if cell['i'] == 0 and cell['j'] == 0: # base case
        return [[]], [[]]
        
    # recursive case

    paths = list()
    alignments = list()
    for pointer in cell['pointers']:
        # compute indexes of neighbor
        if pointer == UP_ARROW:
            i, j = cell['i'] - 1, cell['j']
            action = (cell['s1_seg'], EMPTY)
        elif pointer == LEFT_ARROW:
            i, j = cell['i'], cell['j'] - 1
            action = (EMPTY, cell['s2_seg'])
        elif pointer == DIAG_ARROW:
            i, j = cell['i'] - 1, cell['j'] - 1
            action = (cell['s1_seg'], cell['s2_seg'])

        # follow paths
        for path, acts in zip(*_get_paths(cell=table[i, j], table=table)):
            paths.append([cell] + path)
            alignments.append([action] + acts)

    return paths, alignments

def distance(s1: Union[str, SegStr], s2: Union[str, SegStr]) -> int:
    if isinstance(s1, str):
        s1 = SegStr(segs=s1, seginv=SegInv())
    if isinstance(s2, str):
        s2 = SegStr(segs=s2, seginv=s1._seginv)
    table = _compute_table(s1=s1, s2=s2)
    n, m = len(s1), len(s2)
    return table[n, m]['distance']

def alignments(s1: Union[str, SegStr], s2: Union[str, SegStr]) -> list:
    '''
    '''
    if isinstance(s1, str):
        s1 = SegStr(segs=s1, seginv=SegInv())
    if isinstance(s2, str):
        s2 = SegStr(segs=s2, seginv=s1._seginv)
    n, m = len(s1), len(s2)
    table = _compute_table(s1=s1, s2=s2)
    _, alignment_opers = _get_paths(cell=table[n, m], table=table)
    alignments = list()
    for alignment in alignment_opers:
        aligned_s1 = list()
        aligned_s2 = list()
        for s1_seg, s2_seg in list(reversed(alignment)):
            if type(s1) is str:
                aligned_s1 += s1_seg
                aligned_s2 += s2_seg
            else:
                aligned_s1.append(s1_seg)
                aligned_s2.append(s2_seg)
        alignments.append((SegStr(aligned_s1, s1._seginv), SegStr(aligned_s2, s1._seginv)))

    return alignments

if __name__ == '__main__':
    x = 'vintner'
    y = 'writers'
    print(distance(x, y))
    alignments(x, y)

    x = 'qacdbd'
    y = 'qawxb'
    print(distance(x, y))
    alignments(x, y)
