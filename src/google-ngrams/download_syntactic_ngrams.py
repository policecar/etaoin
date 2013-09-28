#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from https://github.com/piantado/ngrampy/blob/master/download.py

"""
Script to download Google's corpus of syntactic n-grams from 
https://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html

Please note that the README is not included in this download. You can find it at
https://docs.google.com/document/d/14PWeoTkrnKk9H8_7CfVbdvuoFZ7jYivNTkBX2Hj7qLw/edit?usp=sharing

Usage: python download_syntactic_ngrams.py -h
"""

import re
import os
import argparse
import urllib
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

try:
    from IPython import embed
except ImportError:
    pass


def download_syntactic_ngrams( version, corpus, path, filter ):

    base_url    = "http://commondatastorage.googleapis.com/books/syntactic-ngrams/"
    index_page  = "index.html"

    pattern = r"%s/%s" % ( corpus, filter )
    corpus_path = os.path.join( path, corpus )

    # scrape relevant links from the landing /index page
    http = httplib2.Http()
    status, response = http.request( base_url + index_page )

    for link in BeautifulSoup( response, parseOnlyThese=SoupStrainer('a') ):
        
        if link.has_key( 'href' ):
            url = link['href']
            
            # if url matches specified language and version
            match = re.search( pattern, url )
            if match:

                filename    = os.path.basename( url )
                whattype    = match.group(1)
                subdir_path = os.path.join( corpus_path, whattype )
                
                # if directory doesn't exist, make it
                if not os.path.exists( corpus_path ): os.mkdir( corpus_path )
                if not os.path.exists( subdir_path ): os.mkdir( subdir_path )
                
                # if file doesn't exist, download it
                #TODO: add checksum /hash test or some other way to verify file integrity
                file_path = os.path.join( corpus_path, whattype, filename )
                if not os.path.exists( file_path ):
                    try:
                        print "# Downloading %s to %s" % ( url, file_path )
                        urllib.urlretrieve( url, file_path )
                    except urllib.ContentTooShortError:
                        os.remove( file_path )
                        urllib.urlretrieve( url, file_path )


if __name__ == '__main__':

    parser = argparse.ArgumentParser( 
        prog="download_syntactic_ngrams.py",
        description="Download helper for Google's syntactic n-grams." )
    parser.add_argument( '--version', default='20130501', 
        help="specify corpus version to download; default: '20130501'" )
    parser.add_argument( '--corpus', default='eng',
        help="specify which corpus to download; default: 'eng'" )
    parser.add_argument( '--path', default='.',
        help="provide path to store corpus to; defaults to './'" )
    parser.add_argument( '--filter', default='([\w-]+)\.\d\d-of-\d\d\.gz',
        help="regular expression to restrict files downloaded; default: '([\w-]+)\.\d\d-of-\d\d\.gz'" )
    args = parser.parse_args()
    download_syntactic_ngrams( args.version, args.corpus, args.path, args.filter )
