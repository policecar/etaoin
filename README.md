## etaoin

A collection of utilities for natural language processing – includes scripts for downloading, scraping 
and scrubbing open NLP data from the web, some code for pattern extraction, plus a bit of visualization.

Work in progress!


### Contents

Currently contains scripts for 

* downloading Google's [n-grams](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html)
 and [syntactic n-grams](https://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html) 
 ( s.a. [All our n-gram...](http://googleresearch.blogspot.de/2006/08/all-our-n-gram-are-belong-to-you.html)
 and [Syntactic Ngrams over Time](http://googleresearch.blogspot.de/2013/05/syntactic-ngrams-over-time.html) ) 
 and extracting patterns from them using [Pig](https://pig.apache.org/) ≥ 0.12 and CPython UDFs
 to run locally or on a [Hadoop](https://hadoop.apache.org/) cluster.

* visualizing n-grams as mini-graphs: [looking-at-ngrams](https://github.com/policecar/etaoin/tree/master/looking-at-ngrams)

* scraping a Twitter user's timeline ( [twitter](https://github.com/policecar/etaoin/tree/master/twitter) )
  or feeding a .csv file to sqlite and the like ( [utils](https://github.com/policecar/etaoin/tree/master/utils) )

* [web-as-corpus](https://github.com/policecar/etaoin/tree/master/web-as-corpus): a minimal show case using the Wordnik API


### Usage

Check out the subdirectories on how to use each module.

