#!/usr/bin/env python

import HTMLParser
import time

from twitter.oauth import OAuth, read_token_file
from twitter.api import Twitter, TwitterError


# stolen ... need my own at some point in time
CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'

gHtmlParser = HTMLParser.HTMLParser()
_timeZone = None


def getOlsonName() :
	'''
		get the Olson name (timezone) for the local system

	'''
	import os

	olsonName = None

	try :
		olsonName = '/'.join( os.readlink( '/etc/localtime' ).split( '/' )[ -2 : ])
	except OSError :
		from hashlib import sha224

		tzFile = open('/etc/localtime')
		tzFileDigest = sha224( tzFile.read() ).hexdigest()
		tzFile.close()

		for root, dirs, filenames in os.walk( '/usr/share/zoneinfo/' ) :
			for filename in filenames :
				fullname = os.path.join( root, filename )
				f = open( fullname )
				digest = sha224( f.read() ).hexdigest()
				if digest == tzFileDigest:
					olsonName = '/'.join(( fullname.split( '/' ))[ -2 : ])
				f.close()

	return olsonName


def tweeDir() :
	'''
		Create the .twee directory if needed and return the path when finished.

	'''
	import os, os.path

	tweeDir = os.path.expanduser( '~/.twee/' )
	if not os.path.exists( tweeDir ) :
		# create the path
		os.mkdir( tweeDir )

	return tweeDir


def tweePath( options, name ) :
	'''
		Generate a path string for the file name in question

	'''
	import os.path
	return os.path.join( options.tweeDir, name )


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
	parser.add_option( "", "--logPath", dest="logPath", default = '/tmp/',
						help="Directory for the log file" )
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
	setattr( options, 'outFilePath', '%s/%s' % ( options.logPath, options.outFileName ))
	setattr( options, 'tweeDir', tweeDir() )

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
	global _timeZone
	time = tweet[ 'created_at' ]
	if _timeZone is not None :
		from dateutil import parser
		dt = parser.parse( time )
		localDt = dt.astimezone( _timeZone )
		time = localDt.strftime( '%Y-%m-%d %H:%M:%S' )

	info = '@%s (%s in %s) at %s' % (	tweet[ 'user'][ 'screen_name' ],
										tweet[ 'user'][ 'name' ],
										tweet[ 'user'][ 'location' ],
										time )
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
			import datetime
			print datetime.datetime.now()
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

	olsonName = getOlsonName()
	if None is not olsonName :
		from pytz import timezone
		global _timeZone
		_timeZone = timezone( olsonName )

	oauthFile = tweePath( options, 'auth' )
	# should add code to handle the handshake...
	# from twitter.oauth_dance import oauth_dance
	# oauth_dance( "the Command-Line Tool", CONSUMER_KEY, CONSUMER_SECRET, options['oauth_filename'])
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


