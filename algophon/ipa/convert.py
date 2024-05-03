_ipa_to_tipa = {
        # consonants
        'p': 'p',
        'b': 'b',
        't': 't',
        'd': 'd',
        'ʈ': '\\:t',
        'ɖ': '\\:d',
        'c': 'c',
        'ɟ': '\\textbardotlessj',
        'k': 'k',
        'g': 'g', # U+0067; ord('g') == 103
        'ɡ': 'g', # U+0261; ord('ɡ') == 609
        'ɢ': '\\;G',
        'q': 'q',
        'ʔ': 'P',

        'm': 'm',
        'ɱ': 'M',
        'n': 'n',
        'ɳ': '\\:n',
        'ɲ': '\\textltailn',
        'ŋ': 'N',
        'ɴ': '\\;N',

        'ʙ': '\\;B',
        'r': 'r',
        'ʀ': '\\;R',

        'ɾ': 'R',
        'ɽ': '\\:r',

        'ɸ': 'F',
        'β': 'B',
        'f': 'f',
        'v': 'v',
        'θ': 'T',
        'ð': 'D',
        's': 's',
        'z': 'z',
        'ʃ': 'S',
        'ʒ': 'Z',
        'ʂ': '\\:s',
        'ʐ': '\\:z',
        'ç': '\\c{c}',
        'ʝ': 'J',
        'x': 'x',
        'ɣ': 'G',
        'χ': 'X',
        'ʁ': 'K',
        'ħ': '\\textcrh',
        'ʕ': 'Q',
        'h': 'h',
        'ɦ': 'H',

        # other consonants

        'ʘ': '\\!o',
        '|': '|',
        '!': '!',
        'ǂ': '\\textdoublebarpipe',

        '||': '||',
        'ǁ': 'ǁ',

        'ɓ': '\\!b',
        'ɗ': '\\!d',
        'ʄ': '\\!j',
        'ɠ': '\\!g',
        'ʛ': '\\!G',

        'ʍ': '\\*w',
        'ɧ': '\\texththeng',
        'ɕ': 'C',
        'ʑ': '\\textctz',
        'ʜ': '\\;H',
        'ʢ': '\\textbarrevglotstop',
        'ɥ': '4',
        'w': 'w',
        'ɺ': '\\textturnlonglegr',

        # vowels
        'i': 'i',
        'y': 'y',
        'ɪ': 'I',
        'ʏ': 'Y',

        'ɨ': '1',
        'ʉ': '0',

        'ɯ': 'W',
        'u': 'u',
        'ʊ': 'U',

        'e': 'e',
        'ø': '\\o',
        'ɛ': 'E',
        'œ': '\\oe',

        'ɘ': '9',
        'ə': '@',
        'ɜ': '3',
        'ɵ': '8',
        'ʚ': '\\textcloseepsilon',
        
        'ɤ': '7',
        'o': 'o',
        'ʌ': '2',
        'ɔ': 'O',
        
        'æ': '\\ae',
        'ɶ': '\\OE',

        'ɐ': '5',
        'a': 'a',

        'ɑ': 'A',
        'ɒ': '6',

        # various
        't͡s': '\\t{ts}',
        'ʦ': '\\t{ts}',
        'd͡z': '\\t{tz}',
        'ʣ': '\\t{dz}',
        't͡ʃ ': '\\t{tS}',
        'ʧ': '\\t{tS}',
        'd͡ʒ': '\\t{tZ}',
        'ʤ': '\\t{tZ}',

        'ɚ': '\\textrhookschwa',
    }

def to_tipa(segstr):
    '''
    Converts IPA to tipa for LaTeX.
        - \\usepackage{tipa}
        - To use tone letters \\usepackage[tone]{tipa}

    Dictionary based on table https://jon.dehdari.org/tutorials/tipachart_mod.pdf
    '''
    if isinstance(segstr, str):
        segstr = segstr.split()

    tipastr = list()
    for idx, seg in enumerate(segstr):
        if seg not in _ipa_to_tipa:
            print(f'Seg {seg} at index {idx} is not in tipa map, entering "?" instead')
            tipastr.append('?')
        else:
            tipastr.append(_ipa_to_tipa[seg])
            
    return '\\textipa{' + ' '.join(tipastr) + '}'