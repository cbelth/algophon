from algophon.seg import Seg
from algophon.natclass import NatClass
from algophon.symbols import UNDERSPECIFIED

import pkgutil

class SegInv:
    '''
    A class representing an inventory of phonological segments (Seg objects).
    '''
    def __init__(self, 
                 ipa_file_path: str=None, 
                 sep: str='\t'
        ):
        self._ipa_source = f'Panphon (https://github.com/dmort27/panphon)' if ipa_file_path is None else ipa_file_path
        self.ipa_file_path = ipa_file_path # uses Panphon features (https://github.com/dmort27/panphon) by default
        self.sep = sep

        # load the _seg_to_feat_vec map
        self._load_seg_to_feat_dict()

        # stores the Seg objects in the SegInv
        self.segs = set()

        # maps ipa symbols to their Seg object in the SegInv
        self._ipa_to_seg = dict()

    def __str__(self) -> str:
        return f'SegInv of size {len(self)}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self.segs)
    
    def __iter__(self):
        return self.segs.__iter__()
    
    def __contains__(self, seg: object) -> bool:
        '''
        :seg: Can be any of the following:
            - str IPA symbol
            - Seg object

        :return: True if the :seg: is in the alphabet, False if not
        '''
        return seg in self.segs
    
    def __getitem__(self, seg: object) -> Seg:
        '''
        :seg: Can be any of the following:
            - str IPA symbol
            - Seg object

        :return: the Seg object corresponding to :seg: if present, otherwise KeyError is raised
        '''
        if seg not in self:
            raise KeyError(f'{seg} of type {type(seg)} is not in the SegInv (try <seginv_obj>.add({seg}))')
        return self._ipa_to_seg[seg]

    def _load_seg_to_feat_dict(self) -> None:
        self._seg_to_feat_vec = dict()
        data = pkgutil.get_data(__name__, "ipa.txt")

        if self.ipa_file_path is None:
            lines = data.decode('utf-8').strip().split('\n')
        else:
            with open(self.ipa_file_path, 'r') as f:
                lines = f.readlines()
        for i, line in enumerate(lines): # iterate over lines
            line = line.strip().split(self.sep)
            seg, feats = line[0], line[1:] # extract the IPA segment and its features
            if i == 0: # extract the header
                self.feature_space = feats
            else: # add the segment to the dict
                self._seg_to_feat_vec[seg] = feats

        if self.ipa_file_path is None:
            # make ord('g') == 103 and ord('ɡ') == 609 the same, since panphon only as 609
            self._seg_to_feat_vec['g'] = self._seg_to_feat_vec['ɡ']

    def add(self, ipa_seg: str) -> None:
        '''
        :ipa_seg: an IPA segment in str form

        :return: None
        '''
        if ipa_seg in self:
            return
        if ipa_seg not in self._seg_to_feat_vec:
            raise KeyError(f'Segment {ipa_seg} is not in the IPA data from {self._ipa_source}.')
        feat_vec = self._seg_to_feat_vec[ipa_seg] # get the feature vector
        features = dict((feat, feat_vec[idx]) for idx, feat in enumerate(self.feature_space)) # convert the vector to dict form
        seg = Seg(ipa=ipa_seg, features=features)
        self.segs.add(seg)
        self._ipa_to_seg[ipa_seg] = seg

    def add_segs(self, ipa_segs: object) -> None:
        '''
        :ipa_segs: an iterable of IPA segments, each in str form

        :return: None
        '''
        for ipa in ipa_segs:
            self.add(ipa)

    def add_segs_by_str(self, seg_str: str) -> None:
        '''
        :ipa_segs: a str of space-separated IPA segments

        :return: None
        '''
        self.add_segs(seg_str.split())

    def add_and_get(self, seg: object) -> Seg:
        '''
        Useful for adding a str IPA seg and retrieving its Seg object in one action.

        :seg: an IPA segment in str form or a Seg object

        :return: the Seg object corresponding to the IPA seg
        '''
        self.add(f'{seg}')
        return self[seg]
    
    def add_custom(self, symbol: str, features: dict) -> None:
        '''
        Adds a custom symbol (i.e., not one in the IPA inventory used to create the SegInv).
        Useful for abstract segments like /S/ for {[s], [ʃ]}.

        :symbol: A 

        :return: None
        '''
        if symbol in self._seg_to_feat_vec:
            raise ValueError(f'The symbol "{symbol}" is already a symbol in the IPA data from {self._ipa_source}.')
        if set(features.keys()) != set(self.feature_space):
            raise ValueError('The features do not match those in the feature space.')
        seg = Seg(ipa=symbol, features=features)
        self.segs.add(seg)
        self._ipa_to_seg[symbol] = seg
    
    def extension(self, nat_class) -> set:
        '''
        :nat_class: a set of features or a NatClass object

        :return: the extension of the :nat_class:
        '''
        if type(nat_class) is set:
            nat_class = NatClass(nat_class, self)
        return set(seg for seg in self.segs if seg in nat_class)
    
    def extension_complement(self, nat_class) -> set:
        '''
        :nat_class: a set of features or a NatClass object

        :return: the extensional complement of :nat_class: relative to :self: SegInv \ NatClass
        '''
        return self.segs.difference(self.extension(nat_class=nat_class))
    
    def feature_intersection(self, segs, exclude_underspecified: bool=True) -> set:
        '''
        :segs: an iterable of phonological segments
        :exclude_underspecified: if True (default), excludes features that all the segments are underspecified for

        :return: the features shared by all the :segs: (excludes features where all segs are underspecified)
        '''
        segs = set(self[seg] for seg in segs)
        return set.intersection(*list(set(f'{val}{feat}' for feat, val in seg.features.items() if val != UNDERSPECIFIED or not exclude_underspecified) for seg in segs))
    
    def feature_diff(self, seg1, seg2) -> set:
        '''
        :seg1: phonological segment
        :seg2: phonological segment

        :return: the features that differ between :seg1: and :seg2:
        '''
        seg1 = self[seg1]
        seg2 = self[seg2]
        diff = set()
        for feat in self.feature_space:
            if seg1.features[feat] != seg2.features[feat]:
                diff.add(feat)
        return diff