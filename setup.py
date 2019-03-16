from setuptools import setup

setup(
	name='an-python-scripts',
	version='0.1.0',
	scripts=['scripts/app'],
	packages=['app'],
	url='',
	license='license.txt',
	author='Sorondare',
	author_email='',
	description='Program to expose output of a list of console commands',
	data_files=[('config', ['resources/config.ini'])]
)
