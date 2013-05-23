
"""
	setup.py

		Manage the packaging.

"""

from setuptools import setup, find_packages


_longDesc = """
A small twitter client based on the official twitter python libs.
"""
_version = __import__( 'twee' ).__version__


setup (
	name = 'twee',
	version = _version,
	description = 'Basic command line twitter client',
	long_description = _longDesc,
	author = 'Dave Ely',
	author_email='dely@dijatool.com',
	packages = find_packages(),
	license='BSD License',
	install_requires = [ 'python-dateutil>=2.1', 'pytz>=2013b', 'twitter>=1.9.4' ],
	classifiers = [	'Development Status :: 2 - Pre-Alpha',
					'Intended Audience :: Developers',
					'License :: OSI Approved :: BSD License',
					'Natural Language :: English',
					'Programming Language :: Python :: 2.5',
					'Programming Language :: Python :: 2.6',
					'Programming Language :: Python :: 2.7',
					'Programming Language :: Python :: Implementation :: CPython', ],
	)


