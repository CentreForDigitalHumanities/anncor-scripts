# AnnCor-scripts

It is recommended to create a `virtualenv` using Python 3.5 (or higher) before running any of the code.

Then simply:
```bash
$ pip install -r requirements/deploy.txt
$ ./run_tests.sh
```

Run `pip install -r requirements/develop.txt` for setting up the development environment.

All provided tests should run without issues.

## Adding Morphological Information to CHAT Files

Use `./add_mor_to_cha.py` for adding `%mor` tiers to an existing CHAT file. The format expected for the file containing the morphological information is a [Lassy XML](https://www.let.rug.nl/vannoord/Lassy/) file (as produced by [Alpino](https://www.let.rug.nl/vannoord/alp/Alpino/)) which are (a) merged in a single XML under some root node (e.g. `<Treebank>`) and (b) contain a `sentid` attribute in the `<sentence>` tag with a one-based utterance index.

The result will be output to the console. When there are no issues the output can simply be targeted to the desired output file.

```bash
$ ./add_mor_to_cha.py -c example.cha -p example.xml > enriched.cha
```

Missing tag mapping will be output in the results in the form `???|[word]-[lassy tag]`, e.g. `???|niet-BW(init)` if this one for the word "niet" is missing. At the end of the conversion an overview of missing tags is rendered to console as an error. The output file can then be inspected for more contextual information.

```bash
$ ./add_mor_to_cha.py -c example.cha -p example.xml -c incomplete_mapping.csv > enriched.cha
> ERROR 9 sentence(s) have no tag mapping defined!
> ERROR Missing mapping(s):
> BW()
> TSW()
```

These errors could also be written to a file if needed:

```bash
$ ./add_mor_to_cha.py -c example.cha -p example.xml -c incomplete_mapping.csv > enriched.cha 2> errors.log
```

### POS Mapping

The POS mapping can be provided as a comma-separated CSV file using `--mapping` (`-m`). This is used to map each node denoting as single word in the Lassy XML file to a well-formed CHAT tag e.g. `V|help-inf`. The CSV file should contain a header and the following columns:

1. The CHAT tag to place before the word in the `%mor` tier, e.g. `V`. *Optionally* a delimiter (e.g. `-`, `#` or `&`) followed by the affix to use.
2. The ID (ignored).
3. The value in the Lassy `postag` attribute to match.
4. The word form to use (`lemma` or `root`).

Additional columns are ignored.

#### Separable Verbs

Separable verbs are automatically detected and mapped: either placing the preposition separately if its included in the node (e.g. `aan$ V|schaats-PASP`) or removing it when it's not embedded in this node. See `test_separable_verb` for precise details.

#### Punctuation Mapping

Punctuation performed is done when a word is mapped to `PUNCT` e.g.: `PUNCT|period`. Instead of the symbol itself, a mapping is used. A tab-separated CSV file can be provided using `--punctuation` (`-u`), containing:

1. The punctuation symbol to match.
2. The word to use in its place.
