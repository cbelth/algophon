import unittest
import sys

sys.path.append('../')
from algophon.utils import en_syllabify

class TestEnSyllabify(unittest.TestCase):
    def test_en_syllabify(self):
        assert(en_syllabify('AH0 L AE1 S K AH0', transcription='arpabet') == 'AH0.L AE1 S.K AH0')
        assert(en_syllabify('ə l æ s k ə', transcription='ipa') == 'ə.l æ s.k ə')
        assert(en_syllabify('AH0 L AE1 S K AH0'.split(), alaska_rule=False, transcription='arpabet') == 'AH0.L AE1.S K AH0')
        assert(en_syllabify('ə l æ s k ə', alaska_rule=False, transcription='ipa') == 'ə.l æ.s k ə')

        ''' huge medial onsets: '''
        # minstrel
        assert(en_syllabify('M IH1 N S T R AH0 L', transcription='arpabet') == 'M IH1 N.S T R AH0 L')
        assert(en_syllabify('m ɪ n s t r ə l') == 'm ɪ n.s t r ə l')
        # octroi
        assert(en_syllabify('AA1  K T R W AA0 R'.split(), transcription='arpabet') == 'AA1 K.T R W AA0 R')
        assert(en_syllabify('ɑ k t r w ɑ r') == 'ɑ k.t r w ɑ r')

        ''' normal treatment of 'j' '''
        # menu
        assert(en_syllabify('M EH1 N Y UW0', transcription='arpabet') == 'M EH1 N.Y UW0')
        assert(en_syllabify('m ɛ n j uː') == 'm ɛ n.j uː')
        assert(en_syllabify('m ɛ n j u') == 'm ɛ n.j u')
        # spaniel
        assert(en_syllabify('S P AE1 N Y AH0 L', transcription='arpabet') == 'S P AE1 N.Y AH0 L')
        # canyon
        assert(en_syllabify('K AE1 N Y AH0 N', transcription='arpabet') == 'K AE1 N.Y AH0 N')
        # minuet
        assert(en_syllabify('M IH0 N Y UW2 EH1 T', transcription='arpabet') == 'M IH0 N.Y UW2.EH1 T')
        # junior
        assert(en_syllabify('JH UW1 N Y ER0', transcription='arpabet') == 'JH UW1 N.Y ER0')
        # clerihew
        assert(en_syllabify('K L EH R IH HH Y UW', transcription='arpabet') == 'K L EH.R IH.HH Y UW')
        assert(en_syllabify('k l ɛ ɹ ɪ h j u') == 'k l ɛ.ɹ ɪ.h j u')

        ''' nuclear treatment of 'j' '''
        # rescue
        assert(en_syllabify('R EH1 S K Y UW0', transcription='arpabet') == 'R EH1 S.K Y UW0')
        assert(en_syllabify('r ɛ s k j uː') == 'r ɛ s.k j uː')
        assert(en_syllabify('r ɛ s k j u') == 'r ɛ s.k j u')
        # tribute
        assert(en_syllabify('T R IH1 B Y UW0 T', transcription='arpabet') == 'T R IH1 B.Y UW0 T')
        # nebula
        assert(en_syllabify('N EH1 B Y AH0 L AH0', transcription='arpabet') == 'N EH1 B.Y AH0.L AH0')
        # spatula
        assert(en_syllabify('S P AE1 CH UH0 L AH0', transcription='arpabet') == 'S P AE1.CH UH0.L AH0')
        # acumen
        assert(en_syllabify('AH0 K Y UW1 M AH0 N', transcription='arpabet') == 'AH0 K.Y UW1.M AH0 N')
        # succulent
        assert(en_syllabify('S AH1 K Y AH0 L IH0 N T', transcription='arpabet') == 'S AH1 K.Y AH0.L IH0 N T')
        # formula
        assert(en_syllabify('F AO1 R M Y AH0 L AH0', transcription='arpabet') == 'F AO1 R M.Y AH0.L AH0')
        # value
        assert(en_syllabify('V AE1 L Y UW0', transcription='arpabet') == 'V AE1 L.Y UW0')

        ''' everything else '''
        # nostalgic
        assert(en_syllabify('N AO0 S T AE1 L JH IH0 K', transcription='arpabet') == 'N AO0.S T AE1 L.JH IH0 K')
        # churchment
        assert(en_syllabify('CH ER1 CH M AH0 N', transcription='arpabet') == 'CH ER1 CH.M AH0 N')
        # compensate
        assert(en_syllabify('K AA1 M P AH0 N S EY2 T', transcription='arpabet') == 'K AA1 M.P AH0 N.S EY2 T')
        # inCENSE and INcense
        assert(en_syllabify('IH0 N S EH1 N S', transcription='arpabet') == 'IH0 N.S EH1 N S') # inCENSE
        assert(en_syllabify('IH1 N S EH2 N S', transcription='arpabet') == 'IH1 N.S EH2 N S') # INcense
        assert(en_syllabify('ɪ n s ɛ n s') == 'ɪ n.s ɛ n s')
        # ascend
        assert(en_syllabify('AH0 S EH1 N D', transcription='arpabet') == 'AH0.S EH1 N D')
        # rotate
        assert(en_syllabify('R OW1 T EY2 T', transcription='arpabet') == 'R OW1.T EY2 T')
        # artist
        assert(en_syllabify('AA1 R T AH0 S T', transcription='arpabet') == 'AA1 R.T AH0 S T')
        # actor
        assert(en_syllabify('AE1 K T ER0', transcription='arpabet') == 'AE1 K.T ER0')
        # plaster
        assert(en_syllabify('P L AE1 S T ER0', transcription='arpabet') == 'P L AE1 S.T ER0')
        # butter
        assert(en_syllabify('B AH1 T ER0', transcription='arpabet') == 'B AH1.T ER0')
        # camel
        assert(en_syllabify('K AE1 M AH0 L', transcription='arpabet') == 'K AE1.M AH0 L')
        # upper
        assert(en_syllabify('AH1 P ER0', transcription='arpabet') == 'AH1.P ER0')
        # balloon
        assert(en_syllabify('B AH0 L UW1 N', transcription='arpabet') == 'B AH0.L UW1 N')
        # proclaim
        assert(en_syllabify('P R OW0 K L EY1 M', transcription='arpabet') == 'P R OW0.K L EY1 M')
        # insance
        assert(en_syllabify('IH0 N S EY1 N', transcription='arpabet') == 'IH0 N.S EY1 N')
        assert(en_syllabify('ɪ n s eɪ n') == 'ɪ n.s eɪ n')
        # exclude
        assert(en_syllabify('IH0 K S K L UW1 D', transcription='arpabet') == 'IH0 K.S K L UW1 D')
        assert(en_syllabify('ɪ k s k l uː d') == 'ɪ k.s k l uː d')

if __name__ == "__main__":
    unittest.main()