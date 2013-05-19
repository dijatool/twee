#!/usr/bin/env python

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
	from optparse import OptionParser

	usage = "  %prog [options]"
	parser = OptionParser( usage = usage )
	parser.add_option( "-d", "--depth", dest="depth", default = 100,
						help="How big a queue are we going to be using internally?" )
	parser.add_option( "-b", "--background", dest="background", default = False,
						action="store_true",
						help="Which list are we using?" )
	parser.add_option( "", "--list", dest="list", default = None,
						help="Which list are we using?" )
	parser.add_option( "-l", "--logging", dest="saveLog", default = False,
						action="store_true",
						help="Determine if we save a log file." )
	parser.add_option( "", "--outFileName", dest="outFileName", default = 'twitter-log.txt',
						help="What file are we logging to?" )

	( options, args ) = parser.parse_args()

	setattr( options, 'listId', None )
	setattr( options, 'outFile', None )
	setattr( options, 'outFilePath', '%s/%s' % ( '/tmp/', options.outFileName ))

	return options


def getTweets( twitter, options ) :
	'''
		getTweets needs a description...

	'''
	tweets = None
	if None != options.listId :
		tweets = twitter.lists.statuses( list_id = options.listId, count = options.depth )
	else :
		tweets = twitter.statuses.home_timeline( count = options.depth )

	return tweets


def tweetText( tweet ) :
	'''
		tweetText needs a description...

	'''
	info = '%s @%s (%s) on %s' % ( tweet[ 'user'][ 'name' ],
									tweet[ 'user'][ 'screen_name' ],
									tweet[ 'user'][ 'location' ], tweet[ 'created_at' ] )
	text = gHtmlParser.unescape( tweet[ 'text' ])

	return '%s\n%s\n' % ( info, text )


def flush( options ) :
	'''
		flush needs a description...

	'''
	import os
	import sys

	sys.stdout.flush()

	outFile = options.outFile
	if None != outFile :
		if not outFile.closed :
			outFile.flush()
			os.fsync( outFile.fileno() )


def printText( text, options ) :
	'''
		printText needs a description...

	'''
	if not options.background :
		print text

	if None != options.outFile :
		options.outFile.write( '%s\n' % text )


def run( twitter, options ) :
	'''
		run needs a description...

	'''
	import sys
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

		except KeyboardInterrupt :
			sys.exit( 0 )

		except SystemExit :
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
	import os.path
	import traceback

	options = doOptions()

	oauthFile = os.path.expanduser( '.twitter_oauth' )
	oauth_token, oauth_token_secret = read_token_file( oauthFile )

	if options.saveLog :
		options.outFile = codecs.open( options.outFilePath, mode='a', encoding='utf8' )

	twitter = Twitter( auth=OAuth( oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET ),
						api_version='1.1', )

	printText( '-=-=' * 10, options )
	printText( 'Starting @ %s\n' % datetime.datetime.utcnow(), options )

	myLists = twitter.lists.list()
	for aList in myLists :
		if options.list == aList[ 'slug' ] :
			options.listId = aList[ 'id' ]

	setattr( options, 'screen_name', twitter.account.verify_credentials()[ 'screen_name' ] )

	try :
		run( twitter, options )
	except KeyboardInterrupt :
		pass
	except :
		traceback.print_exc()

	if None != options.outFile :
		if not options.outFile.closed :
			options.outFile.close()


if __name__ == "__main__" :
	main()


