from setuptools import setup

setup(
	name='an-python-scripts',
	version='0.1.0',
	scripts=['run.py'],
	packages=['app'],
	url='https://github.com/Sorondare/an-python-scripts',
	author='',
	author_email='',
	license='GNU GENERAL PUBLIC LICENSE Version 3',
	description='Program to expose output of a list of console commands',
	data_files=[('config', ['resources/config.ini'])]
)
