# gretel-scripts

It is recommended to create a `virtualenv` using Python 3.5 (or higher) before running any of the code.

Then simply:
```bash
$ pip install -r requirements.txt
$ ./run_tests.sh
```

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
