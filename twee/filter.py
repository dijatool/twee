#!/usr/bin/env python

'''
	Handle filtering output from twee using various approaches.

	Should add some code to handle pulling of lists...

'''

import re


_tweetStart = re.compile( "@[A-z0-9_\.\-]+ \([^\)]+\) at \d+\-\d+\-\d+ \d+:\d+:\d+" )

_packerPeeps = [
				'Aaron_Nagler',
				'BobMcGinn',
				'BrianCarriveau',
				'coreybehnke',
				'DanKoob',
				'dankasper',
				'EricBaranczyk1',
				'GregABedard',
				'JacobWestendorf',
				'jasonjwilde',
				'JeffAshPG',
				'jrehor',
				'js_packers',
				'KCousineau09',
				'MikeVandermause',
				'N0tAaronRodgers',
				'Packerpedia',
				'PackerRanter',
				'PackerReport',
				'packers',
				'PackerUpdate',
				'Paulimig',
				'PeteDougherty',
				'PGPackersNews',
				'TomSilverstein',
				'TyDunne',
				'WesHod',
				'ZachHeilprin',
				'zachkruse2',
				]


def startsTweet( line ) :
	'''
		startsTweet needs a description...

	'''
	isStart = False
	if _tweetStart.match( line ) :
		isStart = True

	return isStart


def tweetCollector( aSequence ) :
	'''
		Basic generator... collect all lines of a tweet together and allow us to
		do some basic examination of the sender.

	'''
	finished = []
	tweet = []
	for aLine in aSequence :
		aLine = aLine.rstrip()
		if startsTweet( aLine ) :
			yield tweet
			tweet = []
		tweet.append( aLine )
		#print tweet


def doOptions() :
	'''
		Set and load options, tweak config items as needed.

	'''
	from optparse import OptionParser

	usage = "%prog [options]"
	parser = OptionParser( usage = usage )

	parser.add_option( "-v", "--verbose", dest="verbose", default = False, action="store_true",
						help="Spit out extra data?" )

	( options, args ) = parser.parse_args()

	return options


def tweeter( lines ) :
	'''
		Dump the twitter handle for a tweet.

	'''
	hand = re.compile( '[A-z0-9_\.\-]+' )
	handle = None

	match = hand.search( lines[ 0 ] )
	if match :
		handle = lines[ 0 ][ 1 : match.end() ]

	return handle


def main() :
	'''
		Do something useful

		http://stackoverflow.com/questions/11109859/pipe-output-from-shell-command-to-a-python-script

	'''
	import sys

	options = doOptions()
	if not sys.stdin.isatty() :
		input_stream = sys.stdin
	else :
		pass

	for lines in tweetCollector( input_stream ) :
		who = tweeter( lines )
		if who in _packerPeeps :
			for aLine in lines :
				print aLine

if __name__ == '__main__':
	main()


