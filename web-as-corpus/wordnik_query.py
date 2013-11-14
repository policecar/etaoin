"""Minimal show case of the Wordnik API."""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from config import WORDNIK_API_KEY
from wordnik import *


def get_examples( query_term ):
    """Get examples sentences for a query term."""

    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = WORDNIK_API_KEY
    client = swagger.ApiClient(apiKey, apiUrl)

    wordApi = WordApi.WordApi(client)
    examples = wordApi.getExamples( query_term )

    for i in range( 1, len( examples.examples )):
        print examples.examples[i].text
        print 


if __name__ == "__main__":

    parser = argparse.ArgumentParser( description='Project description' )
    parser.add_argument( 'query_term', help='required query term' )
    args = parser.parse_args()
    get_examples( args.query_term )
