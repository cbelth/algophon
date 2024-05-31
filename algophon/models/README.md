# Models

## D2L

An implementation of the model "Distant to Local" from the following [paper](https://cbelth.github.io/public/assets/documents/belth-LI-2024.pdf):

```bibtex
@article{belth2024tiers,
    title={A Learning-Based Account of Phonological Tiers},
    author={Belth, Caleb},
    journal={Linguistic Inquiry},
    year={2024},
    publisher={MIT Press},
    url = {https://doi.org/10.1162/ling\_a\_00530},
}
```

D2L iteratively and abductively constructs tier representations in response to being unable to predict an alternation from adjacent segments.

Here is an example of running the model on a toy consonant harmony dataset.

```pycon
from algophon.models.D2L import D2L

>>> model = D2L() # create a model object
>>> pairs = [ # construct some training pairs
        ('m o k u D', 'm o k u n'), 
        ('a p a D', 'a p a d'),
        ('t u n i D', 't u n i n'),
        ('s o k i D', 's o k i d'),
        ('n i g o D', 'n i g o n'),
        ('u t e D', 'u t e d'),
        ('u m i D', 'u m i n'),
        ('e t e D', 'e t e d'),
        ('u n i b e D', 'u n i b e n'),
        ('k a d u D', 'k a d u d'),
        ('m i t u D', 'm i t u n'),
        ('u n i t a D', 'u n i t a n')
    ]
>>> model.train(pairs)
D2L model with rule Agree({D},{nas,son}) / {n, m} __ ∘ proj(¬[-nas])
>>> model.rule
Agree({D},{nas,son}) / {n, m} __ ∘ proj(¬[-nas])
```

We can see that D2L learned a harmony rule (`Agree`), that leads `/D/` to harmonize in features `{nas,son}` with a `{n, m}` to its left on the tier that exclueds (exclusion indicated by the `¬` symbol) the natural class `[-nas]`.

You can then call the rule (equivalently model) to predict a novel surface form:

```pycon
>>> model('m i k u g a D')
mikugan
>>> model.rule('t u D')
tud
```

The result is a `SegStr` object, which is why it pretty prints without spaces.

Because D2L iteratively changes representations in response to being unable to predict an alternation from adjacent dependencies, if an alternation is sufficiently predictable from adjacent dependencies, no change of representation will occur. This example demonstrates this:

```pycon
>>> pairs = [
        ('m o k u D', 'm o k u d'), 
        ('a p a D', 'a p a d'),
        ('t u n i D', 't u n i t'),
        ('s o k i D', 's o k i t'),
        ('a k D', 'a k t'),
        ('u m i D', 'u m i d'),
    ]
>>> model.train(pairs)
D2L model with rule Agree({D},{voi}) / {u, a, k, i} __
>>> model.rule
Agree({D},{voi}) / {u, a, k, i} __
```

The model learns that /D/ harmonizes in voicing with the segment to its left. Notice that `[t u n i t]` and `[s o k i t]` are exceptions to the generalization. This demonstrates that D2L can tolerate exceptions, which it does via the Tolerance/Sufficiency Principle (TSP; Yang, 2016). You can get the TSP stats, or the rule's accuracy on a set of data, as follows:

```pycon
>>> model.rule.tsp_stats(pairs)
(6, 4) # the rule makes 6 predictions, 4 of which are correct
>> model.rule.accuracy(pairs)
0.6666666666666666
>> model.accuracy(pairs) # the accuracy can be computed directly from the model
0.6666666666666666
```

If you have training data in a file, you can run a model directly on it:

```pycon
>>> model.train_on_file(path=<path_to_data>, sep='\t')
```

The data must contain two columns, separated by `sep`. The first column should be a UR; the second an SR.


### Applications and Limitations

The model currently works with harmony and disharmony, meaning that it can learn alternations involving interactions where the alternating segment takes feature values from some other segment in the environment. In future work, D2L will be extended to model arbitrary relationships (e.g., vowel backness being influenced by the height of a tier-adjacent vowel).

D2L learns a single rule to account for a single alternation. However, PLP (see below) provides a framework for learning multiple rules for multiple alternations. When that model is implemented, it will be possible to plug D2L in to PLP to build a grammar of rules.

## PLP

Comming Soon

## Mɪᴀꜱᴇɢ

An implementation of the model "Meaning Informed Segmentation of Agglutinative Morphology" (Mɪᴀꜱᴇɢ) from the following [paper](https://cbelth.github.io/public/assets/documents/SCiL_2024_Morphological_Segmentation.pdf):

```bibtex
@inproceedings{belth2024miaseg,
  title={Meaning-Informed Low-Resource Segmentation of Agglutinative Morphology},
  author={Belth, Caleb},
  booktitle={Proceedings of the Society for Computation in Linguistics},
  year={2024}
}
```

Mɪᴀꜱᴇɢ morphologically segments agglutinative morphology based on morphological features, exploiting them to identify how differences between closely-related surface forms are marked. Mɪᴀꜱᴇɢ is unsupervised, but requires words be annotated with a set of morphological features. This approach offers the possibility of improvement over unsupervised approaches that operate over only surface forms, while simplifying the data-annotation demands of supervised approaches needing ground-truth segmentations.
For example, Unimorph 3.0 (McCarthy et al.,2020) contains morphological features for 169 languages, but segmentations—via MorphyNet (Batsuren et al., 2021)—for only 15.

Here is an example of running the model on a toy Hungarian dataset (example from the paper). The simplest way to use the model is to segment a given dataset. This can be done via the `train_and_segment` method.

```pycon
from algophon.models.Miaseg import Miaseg

>>> model = Miaseg() # create a model object
>>> triples = [ # construct some training triples
    ('TEACHER', 'tanár', ()),
    ('TEACHER', 'tanárok', ('PL',)),
    ('TEACHER', 'tanároknak', ('PL', 'DAT')),
    ('PERSON', 'személy', ()),
    ('PERSON', 'személynek', ('DAT',)),
]
>>> segmentations = model.train_and_segment(triples)
```

The `train_and_segment` method returns a `list` of `tuple` objects. The `list` contains one entry for each item in the input data, and each `tuple` contains the input triple being segmented (at index `0`), a list of the segmented morphemes (at index `1`), and a `list` analysis/gloss of the segmentation (at index `2`):

```pycon
>>> for in_triple, segmentation, analysis in segmentations:
        print(f'Input {in_triple}\tsegmentation: {segmentation}\tanalysis: {analysis}')
Input ('TEACHER', 'tanár', ())	segmentation: ['tanár']	analysis: ['ROOT']
Input ('TEACHER', 'tanárok', ('PL',))	segmentation: ['tanár', 'ok']	analysis: ['ROOT', 'PL']
Input ('TEACHER', 'tanároknak', ('PL', 'DAT'))	segmentation: ['tanár', 'ok', 'nak']	analysis: ['ROOT', 'PL', 'DAT']
Input ('PERSON', 'személy', ())	segmentation: ['személy']	analysis: ['ROOT']
Input ('PERSON', 'személynek', ('DAT',))	segmentation: ['személy', 'nek']	analysis: ['ROOT', 'DAT']
>>>
```

You can also segment new words with the `segment` method or, equivalently, calling the trained model object directly.

```pycon
>>> model.segment(word='lányoknak', features={'PL', 'DAT'})
(['lány', 'ok', 'nak'], ['ROOT', 'PL', 'DAT'])
>>> model(word='elnöknek', features={'DAT'})
(['elnök', 'nek'], ['ROOT', 'DAT'])
```

If you want to train the model on one set of data and then segment a separate set of data, you can use the `train` method, and then `segment` to segment the new data.

You can also segment IPA data via `SegStr` objects (Mɪᴀꜱᴇɢ builds these for you internally). To do so, pass `use_ipa=True` as a keyword argument to the model constructor.

```pycon
>>> pairs = [
    ('TEACHER', 't ɒ n aː r', ()),
    ('TEACHER', 't ɒ n aː r o k', ('PL',)),
    ('TEACHER', 't ɒ n aː r o k n ɒ k', ('PL', 'DAT')),
    ('PERSON', 's ɛ m eː j', ()),
    ('PERSON', 's ɛ m eː j n ɛ k', ('DAT',)),
]
>>> model = Miaseg(use_ipa=True).train(pairs) # train returns the model object, allowing this one-liner
>>> model.segment('l aː ɲ o k n ɒ k', features={'PL', 'DAT'})
([laːɲ, ok, nɒk], ['ROOT', 'PL', 'DAT'])
>>> model('ɛ l n ø k n ɛ k', features={'DAT'})
([ɛlnøk, nɛk], ['ROOT', 'DAT'])
```

The segmented morphemes are `SegStr` objects, which is why they pretty print without spaces. 

If you have training data in a file, you can run a model directly on it via `train_on_file` (file-based equivalent of `train`) or `train_and_segment_file` (file-based equivalent of `train_and_segment`):

```pycon
>>> segmentations = model.train_and_segment_file(path=<path_to_data>, sep='\t', feature_sep=';')
```

The data should contain three columns, separated by `sep`. The first column should be a unique identifier for the root, the second column the word, and the third column the morphological features (each feature separated by `feature_sep`). By default, `sep='\t'` and `feature_sep=';'`. Notice that this matches Unimorph's data format of three columns (*lemma, inflection, features*).

### Applications and Limitations

The model is designed specifically for agglutinative morphology. Other types of morphology (e.g., fusional concatenation, non-concatenative stem changes, reduplication) would likely require extensions of the model. Please see section 5 of the [paper](https://cbelth.github.io/public/assets/documents/SCiL_2024_Morphological_Segmentation.pdf) for more detailed discussion.

## References

- Yang, C. (2016). *The price of linguistic productivity: How children learn to break the rules of language.* MIT press.
- Arya D McCarthy, Christo Kirov, Matteo Grella, Amrit Nidhi, Patrick Xia, Kyle Gorman, Ekaterina Vylomova, Sabrina J Mielke, Garrett Nicolai, Miikka Silfverberg, et al. (2020). Unimorph 3.0: Universal morphology. In *Proceedings of The 12th language resources and evaluation conference*, pages 3922–3931. European Language Resources Association.
- Khuyagbaatar Batsuren, Gábor Bella, and Fausto Giunchiglia. (2021). Morphynet: a large multilingual database of derivational and inflectional morphology. In *Proceedings of the 18th sigmorphon workshop on computational research in phonetics, phonology, and morphology*, pages 39–48.