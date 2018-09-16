#!/usr/bin/env python
# coding=utf-8

import os, glob
import click

@click.command()
@click.option('--ext', default='torrent')
def cleanup(ext):
	os.chdir('/Users/fatman13/Downloads')

	files = glob.glob('*.{}'.format(ext))
	print('Cleaning.. \'*.{}\' Total {} file(s)'.format(ext, len(files)))

	for file in files:
		try:
			os.remove(file)
			print('removing.. {}'.format(file))
		except OSError:
			print('Warning: OSError..')

if __name__ == '__main__':
	cleanup()