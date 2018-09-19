#!/usr/bin/env python
# coding=utf-8

import click
from pytube import YouTube
from urllib.error import URLError

MAX_RETRIES = 2

proxies1={'https': 'https://127.0.0.1:1080', 
			'http': 'http://127.0.0.1:1080'}
proxies2={'https': 'https://49.99.199.119:443', 
			'http': 'http://49.99.199.119:443'}
proxies3={'https': 'socks5://127.0.0.1:1080', 
			'http': 'socks5://127.0.0.1:1080'}
proxies4={'https': 'socks5://127.0.0.1:1086', 
			'http': 'socks5://127.0.0.1:1086'}
proxies5={'https': 'https://127.0.0.1:1087', 
			'http': 'http://127.0.0.1:1087'}

@click.command()
@click.option('--video', default='jwrr6aIWeus')
@click.option('--path', default='/Users/fatman13/Documents/')
def ytytyt(video, path):

	for i in range(MAX_RETRIES):
		try:
			print('fetching {}'.format(video))
			url = 'https://www.youtube.com/watch?v={}'.format(video)
			# yt = YouTube(url, proxies=proxies1)
			# yt = YouTube(url, proxies=proxies2)
			# yt = YouTube(url, proxies=proxies3)
			# yt = YouTube(url, proxies=proxies4)
			yt = YouTube(url, proxies=proxies5)
		except URLError:
			print('Error: Connection timeout..')
			continue
		else:
			break

	if yt == None:
		print('Error: yt is None.. exit(1)')
		return
	print('Video title: {}'.format(yt.title))

	# streams = yt.streams.all()
	streams = yt.streams.filter(file_extension='mp4').all()

	for i in range(MAX_RETRIES):
		for j, stream in enumerate(streams):
			print('{}: {}'.format(j, stream))

		print('Thumbnail url {}'.format(yt.thumbnail_url))

		num = input('Please choose a stream [0, {}]: '.format(len(streams)-1))
		try:
			num = int(num)
			if num > len(streams):
				print('Error: input too big..')
				continue
		except ValueError:
			print('Error: Wrong input..')
			continue
		else:
			break

	if num >= 0:
		print('Downloading stream {}: {}'.format(num, streams[num]))
		streams[num].download(path)
		print('Downloading done..')

		print('Downloading caption of {}'.format(yt.title))
		caption = yt.captions.get_by_language_code('en')

		filename = '{}{}.srt'.format(path, yt.title)
		with open(filename, 'w') as fd:
			try:
				print(caption.generate_srt_captions(), file=fd)
				print('{}{}.srt created..'.format(path, yt.title))
			except AttributeError:
				print('This video has no caption..')
			

if __name__ == '__main__':
	ytytyt()