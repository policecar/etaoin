#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from https://github.com/piantado/ngrampy/blob/master/download.py

"""
Script to download Google's corpus of syntactic n-grams from 
https://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html.

Please note that the README is not included in this download. You can find it at
https://docs.google.com/document/d/14PWeoTkrnKk9H8_7CfVbdvuoFZ7jYivNTkBX2Hj7qLw/edit?usp=sharing.
"""

import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import os
import urllib

# from IPython import embed

version 	= "20130501"
corpus		= "eng"  # corpora: eng, eng-1M, eng-fiction, eng-us, eng-gb

base_url 	= "http://commondatastorage.googleapis.com/books/syntactic-ngrams/"
index_page 	= "index.html"
pattern 	= r"%s/([\w-]+)\.\d\d-of-\d\d\.gz" % corpus

# scrape relevant links from the landing /index page
http = httplib2.Http()
status, response = http.request( base_url + index_page )

for link in BeautifulSoup( response, parseOnlyThese=SoupStrainer('a') ):
	
	if link.has_key( 'href' ):
		url = link['href']
		
		# if url matches specified language and version
		match = re.search( pattern, url )
		if match:

			filename = os.path.basename( url )
			whattype = match.group(1)			
			subdir = os.path.join( corpus, whattype )
			
			# if directory doesn't exist, make it
			if not os.path.exists( corpus ): os.mkdir( corpus )
			if not os.path.exists( subdir ): os.mkdir( subdir )
			
			# if file doesn't exist, download it
			#TODO: add checksum /hash test or some other way to verify file integrity
			filepath = os.path.join( corpus, whattype, filename )
			if not os.path.exists( filepath ):
				try:
					print "# Downloading %s to %s" % ( url, filepath )
					urllib.urlretrieve( url, filepath )
				except urllib.ContentTooShortError:
					os.remove( filepath )
					urllib.urlretrieve( url, filepath )
