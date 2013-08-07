## looking-at-ngrams

A visualization of n-grams as mini-graphs – based on [d3.js](http://d3js.org/) 
and [force-based label placement](http://bl.ocks.org/MoritzStefaner/1377729).

![sample](https://raw.github.com/policecar/scrubs/master/looking-at-ngrams/take.png)


### Usage

Open `index.html` in a browser (tested for Firefox Aurora 23.0a2), then use the file 
selector to load some data from disk. The data should formatted as follows:

* a single, space-separated n-gram per line followed by its (absolute) count
* if sorted alphabetically, counts can be visualized correctly

e.g. 

`look about oneself 3698` <br>
`take a nap 31507`

