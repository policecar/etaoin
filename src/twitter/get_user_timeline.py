#! /usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from https://github.com/mongolab/twitter-harvest

##############################################################################
#
# Copyright (c) 2013 ObjectLabs Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
################################################################################


import oauth2 as oauth
import urllib2, json
import argparse
import os, sys, time

from config import *


def oauth_header( url, consumer, token ):

    params =  {
        'oauth_version': '1.0',
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time()),
    }
    req = oauth.Request( method = 'GET',url = url, parameters = params )
    req.sign_request( oauth.SignatureMethod_HMAC_SHA1(), consumer, token )
    return req.to_header()['Authorization'].encode('utf-8')


def main():

    ### build arg parser
    parser = argparse.ArgumentParser( description = 'Connects to Twitter user timeline endpoint, retrieves tweets and saves them to file.' )
    parser.add_argument( '-r', '--retweet', help = 'include native retweets in the harvest', action = 'store_true' )
    parser.add_argument( '-v', '--verbose', help = 'print harvested tweets in shell', action = 'store_true' )
    parser.add_argument( '--numtweets', help = 'set total number of tweets to be harvested, max = 3200', type = int, default = 3200 )
    parser.add_argument( '--user', help = 'choose twitter user timeline for harvest', required = True )
    parser.add_argument( '--filename', help = 'filename to save tweets to; user_datetime if omitted' )

    ### fields for query
    args = parser.parse_args()
    user = args.user 
    numtweets = args.numtweets
    verbose = args.verbose
    retweet = args.retweet

    ### build endpoint + set headers
    # note: signature imported from config.py
    base_url = url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?include_entities=true&count=200&screen_name=%s&include_rts=%s' % ( user, retweet )
    oauth_consumer = oauth.Consumer( key = CONSUMER_KEY, secret = CONSUMER_SECRET )
    oauth_token = oauth.Token( key = ACCESS_TOKEN, secret = ACCESS_SECRET )

    ### set filename, if not provided
    filename = args.filename
    if filename == None:
        current_time = time.strftime( "%y%m%d%H%M%S" )
        filename = '_'.join([ 'tw', user, current_time ])
        if not os.path.exists( DIRECTORY ):
            os.makedirs( DIRECTORY )
        filename = os.path.join( DIRECTORY, filename )

    ### helper variables
    max_id = -1

    ### begin the harvest
    while True:
        auth = oauth_header( url, oauth_consumer, oauth_token )
        headers = { "Authorization": auth }
        request = urllib2.Request( url, headers = headers )
        try:
            stream = urllib2.urlopen( request )
        except urllib2.HTTPError, err:
            if err.code == 404:
                print 'Error: Unknown user. Check --user arg'
                return
            if err.code == 401:
                print 'Error: Unauthorized. Check Twitter credentials'
                return
        tweet_list = json.load( stream )

        if len( tweet_list ) == 0:
            print 'No tweets to harvest!'
            return
        if 'errors' in tweet_list:
            print 'Hit rate limit, code: %s, message: %s' % ( tweets['errors']['code'], tweets['errors']['message'] )
            return
        if max_id == -1:
            tweets = tweet_list
        else:
            tweets = tweet_list[1:]
            if len( tweets ) == 0:
                print 'Finished Harvest!'
                return

        with open( filename, 'w' ) as f:
            f.writelines( "%s\n" % tweet for tweet in tweets )
        return


if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        if e.code == 0:
            pass
