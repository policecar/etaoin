## scrubs

Tools for scraping and scrubbing open NLP data from the Web.

### Contents

Currently contains scripts for 

* downloading Google's [n-grams](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html)
 and [syntactic n-grams](https://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html)  
 (cf. [All our n-gram are belong to you](http://googleresearch.blogspot.de/2006/08/all-our-n-gram-are-belong-to-you.html)
 and [Syntactic Ngrams over Time](http://googleresearch.blogspot.de/2013/05/syntactic-ngrams-over-time.html)
 for further description of the data)

* visualizing n-grams as mini-graphs – [looking-at-ngrams](https://github.com/policecar/scrubs/tree/master/src/looking-at-ngrams)


### Usage

Run `python download_ngrams.py` to download Google's n-gram corpus for 'eng-all', version '20120701' 
or else changes the values of $language and $version at the top of the file for a different set of 
languages and version.

Run `python download_syntactic_ngrams.py` to download version '20130501' and 'eng' (all) of the corpus 
of dependency tree fragments.
