#!/usr/bin/env python

import os
import os.path
import sys
import HTMLParser
import time

from twitter.oauth import OAuth, read_token_file
from twitter.api import Twitter, TwitterError


# stolen ... need my own at some point in time
CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'

gHtmlParser = HTMLParser.HTMLParser()


def doOptions() :
	'''
		doOptions needs a description...

	'''
	options = {}

	options[ 'depth' ] = 100
	options[ 'list' ] = 'nfl'

	options[ 'outFile' ] = None

	options[ 'outFileName' ] = 'twitter-log.txt'
	options[ 'outFilePath' ] = '%s/%s' % ( '/tmp/', options[ 'outFileName' ] )


	return options


def getTweets( twitter, options ) :
	'''
		getTweets needs a description...

	'''
	tweets = twitter.lists.statuses( list_id = options[ 'list-id' ], count = options[ 'depth' ] )

	return tweets


def tweetText( tweet ) :
	'''
		tweetText needs a description...

	'''
	info = '%s @%s (%s) on %s' % ( tweet[ 'user'][ 'name' ], tweet[ 'user'][ 'screen_name' ], tweet[ 'user'][ 'location' ], tweet[ 'created_at' ] )
	text = gHtmlParser.unescape( tweet[ 'text' ])

	return '%s\n%s\n' % ( info, text )


def flush( options ) :
	'''
		flush needs a description...

	'''
	sys.stdout.flush()

	outFile = options[ 'outFile' ]
	if None != outFile :
		if not outFile.closed :
			outFile.flush()
			os.fsync( outFile.fileno() )


def printText( text, options ) :
	'''
		printText needs a description...

	'''
	print text

	outFile = options[ 'outFile' ]
	if None != outFile :
		outFile.write( '%s\n' % text )


def run( twitter, options ) :
	'''
		run needs a description...

	'''
	import traceback

	seen = []
	while True :
		try :
			tweets = reversed( getTweets( twitter, options ))
			newTweets = []
			for aTweet in tweets :
				text = tweetText( aTweet )
				if text not in seen :
					printText( text, options )

				newTweets.append( text )
			seen = newTweets
		except ( KeyboardInterrupt, SystemExit ) :
			raise
		except :
			traceback.print_exc()

		flush( options )

		time.sleep( 60 )


def main() :
	'''
		main needs a description...

	'''
	import codecs
	import datetime

	options = doOptions()

	oauthFile = os.path.expanduser( '.twitter_oauth' )
	oauth_token, oauth_token_secret = read_token_file( oauthFile )

	options[ 'outFile' ] = codecs.open( options[ 'outFilePath' ], mode='a', encoding='utf8' )

	twitter = Twitter( auth=OAuth( oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET ),
						api_version='1.1', )

	printText( '-=-=' * 10, options )
	printText( 'Starting @ %s\n' % datetime.datetime.utcnow(), options )

	myLists = twitter.lists.list()
	for aList in myLists :
		if options[ 'list' ] == aList[ 'slug' ] :
			options[ 'list-id' ] = aList[ 'id' ]

	options[ 'screen_name ' ] = twitter.account.verify_credentials()[ 'screen_name' ]
	run( twitter, options )

	outFile = options[ 'outFile' ]
	if None != outFile :
		if not outFile.closed :
			outFile.close()


if __name__ == "__main__" :
	main()



