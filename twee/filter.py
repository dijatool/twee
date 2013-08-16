#!/usr/bin/env python

'''
	Handle filtering output from twee using various approaches.

	Should add some code to handle pulling of lists...

'''

import re


_tweetStart = re.compile( "@[A-z0-9_\.\-]+ \([^\)]+\) at \d+\-\d+\-\d+ \d+:\d+:\d+" )

_packerPeeps = [
					'_EatMoreCheese',
					'_G_Tom',
					'Aaron_Nagler',
					'AaronRodgers12',
					'abevanderbent',
					'adamczech',
					'adbrandt',
					'AhmanGreen30',
					'AlBracco_OSCC',
					'AlexTallitsch',
					'alharris31',
					'alonzohighsmith',
					'Amy__Bailey',
					'bjohnson613',
					'BobMcGinn',
					'BradyPoppinga',
					'BrianCarriveau',
					'buzzboy3',
					'ByChrisJenkins',
					'CBSPackers',
					'ChadToporski',
					'CheeseheadHaven',
					'codybaertschi',
					'coreybehnke',
					'crichar3',
					'DailyDopeSheet',
					'dankasper',
					'DanKoob',
					'eliotwolf46',
					'epmckenna',
					'EricBaranczyk1',
					'frogmandan61',
					'GilbertBrown',
					'gmatzek',
					'goldielocks1966',
					'GregABedard',
					'GrumpyDonHutson',
					'HairHatGuy',
					'hammen',
					'HelpIamaCabbage',
					'JacobWestendorf',
					'jasonjwilde',
					'JasonPerone',
					'JeffAshPG',
					'JerryKramer64GB',
					'JerseyAlGBP',
					'jrehor',
					'js_packers',
					'JTWahlers',
					'Justin_Felder',
					'justismosqueda',
					'jwolf84',
					'KCousineau09',
					'khazaert',
					'KrisLBurke',
					'lanceallan',
					'leap36',
					'leroybutler',
					'lofton80',
					'lombardiave',
					'LoriNickel',
					'MattBowen41',
					'MikeVandermause',
					'N0tAaronRodgers',
					'ngoddardwfrv',
					'nickdapick36',
					'NotVicKetchman',
					'Olivia_Harlan',
					'PackerInsanity',
					'Packerpedia',
					'PackerRanter',
					'PackerReport',
					'packers',
					'PackersTherapy',
					'PackerUpdate',
					'packfansince89',
					'Paulimig',
					'PeteDougherty',
					'PGevansiegle',
					'PGPackersNews',
					'PJHotel_',
					'pocketdoppler',
					'railbirdcentral',
					'RichGannon12',
					'RobDemovsky',
					'robreischel',
					'rug_PhD12',
					'ScottVenci',
					'SeifertESPN',
					'Sparta_Chris',
					'StribDW',
					'Talking1265',
					'TexWestern',
					'TheInsiders_GB',
					'ThePackerFan',
					'ToddMcMahon23',
					'TomOatesWSJ',
					'TomSilverstein',
					'totalpackers',
					'TundraVision',
					'TyDunne',
					'wallypingel',
					'waynelarrivee',
					'WesHod',
					'WillieDavis87',
					'Willwaukee',
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


