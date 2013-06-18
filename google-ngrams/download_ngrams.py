#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from https://github.com/piantado/ngrampy/blob/master/download.py

"""
Script to selectively download google ngram data from 
http://storage.googleapis.com/books/ngrams/books/datasetsv2.html.
"""

import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import os
import urllib

# from IPython import embed

version 	= "20120701"
language 	= "eng-all"
# languages: eng-all, eng-us-all, eng-gb-all, fre-all, ger-all, heb-all, ita-all, rus-all, spa-all

base_url 	= "http://storage.googleapis.com/books/ngrams/books/"
index_page 	= "datasetsv2.html"
pattern		= r"googlebooks-%s-([\d\w]+)-%s" % ( language, version )

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
			whatgram = match.group(1)			
			subdir = os.path.join( language, whatgram )
			
			# if directory doesn't exist, make it
			if not os.path.exists( language ):	os.mkdir( language )
			if not os.path.exists( subdir ): 	os.mkdir( subdir )
			
			# if file doesn't exist, download it
			#TODO: add checksum /hash test or some other way to verify file integrity
			filepath = os.path.join( language, whatgram, filename )
			if not os.path.exists( filepath ):
				try:
					print "# Downloading %s to %s" % ( url, filepath )
					urllib.urlretrieve( url, filepath )
				except urllib.ContentTooShortError:
					os.remove( filepath )
					urllib.urlretrieve( url, filepath )
