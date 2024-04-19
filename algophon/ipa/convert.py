_ipa_to_tipa = {
        'p': 'p',
        'b': 'b',
        't': 't',
        'd': 'd',
        'ʈ': '\\:t',
        'ɖ': '\\:d',
        'c': 'c',
        'ɟ': '\\textbardotlessj',
        'k': 'k',
        'g': 'g', # ord('g') == 103
        'ɡ': 'g', # ord('ɡ') == 609
        'ɢ': '\\;G',
        'q': 'q',
        'ʔ': 'P',

        'm': 'm',
        'ɱ': 'M',
        'n': 'n',
        'ɳ': '\\:n',
        'ɲ': '\\textltailn',
        'ŋ': 'N',
        'ɴ': '\;N',

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

        # TODO: finish
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