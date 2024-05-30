# Models

## D2L

An implementation of the model "Distant to Local" from the following paper:

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

Comming Soon

```bibtex
@inproceedings{belth2024miaseg,
  title={Meaning-Informed Low-Resource Segmentation of Agglutinative Morphology},
  author={Belth, Caleb},
  booktitle={Proceedings of the Society for Computation in Linguistics},
  year={2024}
}
```

## References

- Yang, C. (2016). *The price of linguistic productivity: How children learn to break the rules of language.* MIT press.