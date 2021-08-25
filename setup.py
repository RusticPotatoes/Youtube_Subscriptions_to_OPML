import setuptools
from setuptools import setup
import os 

parent_dir = os.path.dirname(os.path.realpath(__file__))

setup(
	name='',
	version='1.0',
	description='',
	author='',
	author_email='',
	url='',
	python_requires='>=3.8',
	#package_dir={'GEPrediction-OSRS': parent_dir},
	install_requires=[
		'youtube_api',
		'pandas',
		'os',
		'argparse'
		]
	)