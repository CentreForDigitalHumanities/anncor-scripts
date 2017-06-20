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
