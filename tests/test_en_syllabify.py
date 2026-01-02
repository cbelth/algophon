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
        assert(en_syllabify('s p æ n j ə l') == 's p æ n.j ə l')
        # canyon
        assert(en_syllabify('K AE1 N Y AH0 N', transcription='arpabet') == 'K AE1 N.Y AH0 N')
        assert(en_syllabify('k æ n j ə n') == 'k æ n.j ə n')
        # minuet
        assert(en_syllabify('M IH0 N Y UW2 EH1 T', transcription='arpabet') == 'M IH0 N.Y UW2.EH1 T')
        assert(en_syllabify('m ɪ n j uː ɛ t') == 'm ɪ n.j uː.ɛ t')
        assert(en_syllabify('m ɪ n j u ɛ t') == 'm ɪ n.j u.ɛ t')
        # junior
        assert(en_syllabify('JH UW1 N Y ER0', transcription='arpabet') == 'JH UW1 N.Y ER0')
        assert(en_syllabify('dʒ uː n j ɝ') == 'dʒ uː n.j ɝ')
        assert(en_syllabify('dʒ uː n j ɚ') == 'dʒ uː n.j ɚ')
        assert(en_syllabify('dʒ uː n j ɹ̩') == 'dʒ uː n.j ɹ̩')
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
        assert(en_syllabify('t r ɪ b j uː t') == 't r ɪ b.j uː t')
        # nebula
        assert(en_syllabify('N EH1 B Y AH0 L AH0', transcription='arpabet') == 'N EH1 B.Y AH0.L AH0')
        assert(en_syllabify('n ɛ b j ə l ə') == 'n ɛ b.j ə.l ə')
        # spatula
        assert(en_syllabify('S P AE1 CH UH0 L AH0', transcription='arpabet') == 'S P AE1.CH UH0.L AH0')
        assert(en_syllabify('s p æ tʃ ʊ l ə') == 's p æ.tʃ ʊ.l ə')
        assert(en_syllabify('s p æ t͡ʃ ʊ l ə') == 's p æ.t͡ʃ ʊ.l ə')
        # acumen
        assert(en_syllabify('AH0 K Y UW1 M AH0 N', transcription='arpabet') == 'AH0 K.Y UW1.M AH0 N')
        assert(en_syllabify('ə k j uː m ə n') == 'ə k.j uː.m ə n')
        assert(en_syllabify('ə k j u m ə n') == 'ə k.j u.m ə n')
        # succulent
        assert(en_syllabify('S AH1 K Y AH0 L IH0 N T', transcription='arpabet') == 'S AH1 K.Y AH0.L IH0 N T')
        assert(en_syllabify('s ʌ k j ə l ɪ n t') == 's ʌ k.j ə.l ɪ n t')
        # formula
        assert(en_syllabify('F AO1 R M Y AH0 L AH0', transcription='arpabet') == 'F AO1 R M.Y AH0.L AH0')
        assert(en_syllabify('f ɔ r m j ə l ə') == 'f ɔ r m.j ə.l ə')
        # value
        assert(en_syllabify('V AE1 L Y UW0', transcription='arpabet') == 'V AE1 L.Y UW0')
        assert(en_syllabify('v æ l j uː') == 'v æ l.j uː')
        assert(en_syllabify('v æ l j u') == 'v æ l.j u')

        ''' everything else '''
        # nostalgic
        assert(en_syllabify('N AO0 S T AE1 L JH IH0 K', transcription='arpabet') == 'N AO0.S T AE1 L.JH IH0 K')
        assert(en_syllabify('n ɔ s t æ l dʒ ɪ k') == 'n ɔ.s t æ l.dʒ ɪ k')
        assert(en_syllabify('n ɔ s t æ l d͡ʒ ɪ k') == 'n ɔ.s t æ l.d͡ʒ ɪ k')
        # churchment
        assert(en_syllabify('CH ER1 CH M AH0 N', transcription='arpabet') == 'CH ER1 CH.M AH0 N')
        assert(en_syllabify('tʃ ɝː tʃ m ɛ n t') == 'tʃ ɝː tʃ.m ɛ n t')
        assert(en_syllabify('t͡ʃ ɝː tʃ m ɛ n t') == 't͡ʃ ɝː tʃ.m ɛ n t')
        assert(en_syllabify('tʃ ɝː t͡ʃ m ɛ n t') == 'tʃ ɝː t͡ʃ.m ɛ n t')
        assert(en_syllabify('tʃ ɚː tʃ m ɛ n t') == 'tʃ ɚː tʃ.m ɛ n t')
        assert(en_syllabify('tʃ ɹ̩ tʃ m ɛ n t') == 'tʃ ɹ̩ tʃ.m ɛ n t')
        assert(en_syllabify('tʃ ɝ t͡ʃ m ɛ n t') == 'tʃ ɝ t͡ʃ.m ɛ n t')
        assert(en_syllabify('tʃ ɚ tʃ m ɛ n t') == 'tʃ ɚ tʃ.m ɛ n t')
        assert(en_syllabify('tʃ ɹ̩ tʃ m ɛ n t') == 'tʃ ɹ̩ tʃ.m ɛ n t')
        assert(en_syllabify('t͡ʃ ɚ t͡ʃ m ɛ n t') == 't͡ʃ ɚ t͡ʃ.m ɛ n t')
        # compensate
        assert(en_syllabify('K AA1 M P AH0 N S EY2 T', transcription='arpabet') == 'K AA1 M.P AH0 N.S EY2 T')
        assert(en_syllabify('k ɑː m p ə n s eɪ t') == 'k ɑː m.p ə n.s eɪ t')
        assert(en_syllabify('k ɑ m p ə n s eɪ t') == 'k ɑ m.p ə n.s eɪ t')
        assert(en_syllabify('k ɑː m p ə n s eː t') == 'k ɑː m.p ə n.s eː t')
        assert(en_syllabify('k ɑ m p ə n s e t') == 'k ɑ m.p ə n.s e t')
        # inCENSE and INcense
        assert(en_syllabify('IH0 N S EH1 N S', transcription='arpabet') == 'IH0 N.S EH1 N S') # inCENSE
        assert(en_syllabify('IH1 N S EH2 N S', transcription='arpabet') == 'IH1 N.S EH2 N S') # INcense
        assert(en_syllabify('ɪ n s ɛ n s') == 'ɪ n.s ɛ n s')
        # ascend
        assert(en_syllabify('AH0 S EH1 N D', transcription='arpabet') == 'AH0.S EH1 N D')
        assert(en_syllabify('ə s ɛ n d') == 'ə.s ɛ n d')
        # rotate
        assert(en_syllabify('R OW1 T EY2 T', transcription='arpabet') == 'R OW1.T EY2 T')
        assert(en_syllabify('r oʊ t eɪ t') == 'r oʊ.t eɪ t')
        assert(en_syllabify('r o t eɪ t') == 'r o.t eɪ t')
        assert(en_syllabify('r oʊ t e t') == 'r oʊ.t e t')
        assert(en_syllabify('r o t e t') == 'r o.t e t')
        assert(en_syllabify('r oː t eː t') == 'r oː.t eː t')
        assert(en_syllabify('ɹ oʊ t eɪ t') == 'ɹ oʊ.t eɪ t')
        assert(en_syllabify('ɹ o t eɪ t') == 'ɹ o.t eɪ t')
        assert(en_syllabify('ɹ oʊ t e t') == 'ɹ oʊ.t e t')
        assert(en_syllabify('ɹ o t e t') == 'ɹ o.t e t')
        assert(en_syllabify('ɹ oː t eː t') == 'ɹ oː.t eː t')
        # artist
        assert(en_syllabify('AA1 R T AH0 S T', transcription='arpabet') == 'AA1 R.T AH0 S T')
        assert(en_syllabify('ɑː r t ə s t') == 'ɑː r.t ə s t')
        assert(en_syllabify('ɑ r t ə s t') == 'ɑ r.t ə s t')
        assert(en_syllabify('ɑː r t ɪ s t') == 'ɑː r.t ɪ s t')
        assert(en_syllabify('ɑ r t ɪ s t') == 'ɑ r.t ɪ s t')
        assert(en_syllabify('ɑː ɹ t ə s t') == 'ɑː ɹ.t ə s t')
        assert(en_syllabify('ɑ ɹ t ə s t') == 'ɑ ɹ.t ə s t')
        assert(en_syllabify('ɑː ɹ t ɪ s t') == 'ɑː ɹ.t ɪ s t')
        assert(en_syllabify('ɑ ɹ t ɪ s t') == 'ɑ ɹ.t ɪ s t')
        # actor
        assert(en_syllabify('AE1 K T ER0', transcription='arpabet') == 'AE1 K.T ER0')
        assert(en_syllabify('æ k t ɝ') == 'æ k.t ɝ')
        assert(en_syllabify('æ k t ɚ') == 'æ k.t ɚ')
        assert(en_syllabify('æ k t ɹ̩') == 'æ k.t ɹ̩')
        # plaster
        assert(en_syllabify('P L AE1 S T ER0', transcription='arpabet') == 'P L AE1 S.T ER0')
        assert(en_syllabify('p l æ s t ɝ') == 'p l æ s.t ɝ')
        assert(en_syllabify('p l æ s t ɚ') == 'p l æ s.t ɚ')
        assert(en_syllabify('p l æ s t ɹ̩') == 'p l æ s.t ɹ̩')
        # butter
        assert(en_syllabify('B AH1 T ER0', transcription='arpabet') == 'B AH1.T ER0')
        assert(en_syllabify('b ʌ t ɝ') == 'b ʌ.t ɝ')
        assert(en_syllabify('b ʌ t ɚ') == 'b ʌ.t ɚ')
        assert(en_syllabify('b ʌ t ɹ̩') == 'b ʌ.t ɹ̩')
        # camel
        assert(en_syllabify('K AE1 M AH0 L', transcription='arpabet') == 'K AE1.M AH0 L')
        assert(en_syllabify('k æ m ə l') == 'k æ.m ə l')
        # upper
        assert(en_syllabify('AH1 P ER0', transcription='arpabet') == 'AH1.P ER0')
        assert(en_syllabify('ʌ p ɝ') == 'ʌ.p ɝ')
        assert(en_syllabify('ʌ p ɚ') == 'ʌ.p ɚ')
        assert(en_syllabify('ʌ p ɹ̩') == 'ʌ.p ɹ̩')
        # balloon
        assert(en_syllabify('B AH0 L UW1 N', transcription='arpabet') == 'B AH0.L UW1 N')
        assert(en_syllabify('b ə l uː n') == 'b ə.l uː n')
        assert(en_syllabify('b ə l u n') == 'b ə.l u n')
        # proclaim
        assert(en_syllabify('P R OW0 K L EY1 M', transcription='arpabet') == 'P R OW0.K L EY1 M')
        assert(en_syllabify('p r oʊ k l eɪ m') == 'p r oʊ.k l eɪ m')
        assert(en_syllabify('p ɹ oʊ k l eɪ m') == 'p ɹ oʊ.k l eɪ m')
        assert(en_syllabify('p r o k l eɪ m') == 'p r o.k l eɪ m')
        assert(en_syllabify('p ɹ o k l eɪ m') == 'p ɹ o.k l eɪ m')
        assert(en_syllabify('p r oʊ k l e m') == 'p r oʊ.k l e m')
        assert(en_syllabify('p ɹ oʊ k l e m') == 'p ɹ oʊ.k l e m')
        assert(en_syllabify('p r o k l e m') == 'p r o.k l e m')
        assert(en_syllabify('p ɹ o k l e m') == 'p ɹ o.k l e m')
        # insance
        assert(en_syllabify('IH0 N S EY1 N', transcription='arpabet') == 'IH0 N.S EY1 N')
        assert(en_syllabify('ɪ n s eɪ n') == 'ɪ n.s eɪ n')
        # exclude
        assert(en_syllabify('IH0 K S K L UW1 D', transcription='arpabet') == 'IH0 K.S K L UW1 D')
        assert(en_syllabify('ɪ k s k l uː d') == 'ɪ k.s k l uː d')

if __name__ == "__main__":
    unittest.main()