## scrubs

Tools for scraping and scrubbing open NLP data from the Web.

### Contents

Currently contains scripts for downloading two data sets from Google:
* [n-grams](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html)
(see [All our n-gram are belong to you](http://googleresearch.blogspot.de/2006/08/all-our-n-gram-are-belong-to-you.html)
 for a description)
* [syntactic n-grams](https://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html)
(see [Syntactic n-grams over time](http://googleresearch.blogspot.de/2013/05/syntactic-ngrams-over-time.html) 
 for more details)


### Usage

Run `python download_ngrams.py` to download Google's n-gram corpus for 'eng-all', version '20120701' 
or else changes the values of $language and $version at the top of the file for a different set of 
languages and version.

Run `python download_syntactic_ngrams.py` to download version '20130501' and 'eng' (all) of the corpus 
of dependency tree fragments.
