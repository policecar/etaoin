### Google n-grams

#### Data download

Download [Google's n-gram corpus](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html):
```python 
# corpus 'eng-all', version '20120701'
python download_ngrams.py

# adapt the variables <language> and <version> for different combinations
``` 

Download [Google's syntactic n-grams](https://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html) 
aka dependency tree fragments:
```python 
# corpus 'eng', version '20130501', all files
python download_syntactic_ngrams.py

# for further usage details
python download_syntactic_ngrams.py -h
``` 


#### Pattern extraction from syntactic n-grams

Extract patterns from Google's syntactic n-grams (tested for nounargs), e.g. 
```text
earth   {___} may be natural    16 
```
Prerequisites: Pig 0.12 or later

```bash
cd .../etaoin/google-ngrams/pig

# run locally
pig --x local minimize_input.pig
pig --x local extract_patterns.pig

# run on a Hadoop cluster
pig minimize_input.pig
pig extract_patterns.pig
```

