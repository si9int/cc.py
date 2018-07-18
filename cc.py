#!/usr/bin/env python3

import requests, json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('domain', help = 'domain which will be crawled for', type = str)
parser.add_argument('-y', '--year', help = 'limit the result to a specific year (default: all)', type = str)
parser.add_argument('-o', '--out', help = 'specify an output file (default: domain.txt)', type = str)

args = parser.parse_args()
links = []
out = ''

if args.out:
	result = open('./' + args.out, 'w')
	output = str(args.out)
else:
	result = open('./' + args.domain + '.txt', 'w')
	output = str(args.domain + '.txt')

indexes = {
	'y18' : [
		'CC-MAIN-2018-17',
		'CC-MAIN-2018-13',
		'CC-MAIN-2018-09',
		'CC-MAIN-2018-05'
	],
	'y17' : [
		'CC-MAIN-2017-51',
		'CC-MAIN-2017-47',
		'CC-MAIN-2017-43',
		'CC-MAIN-2017-39',
		'CC-MAIN-2017-34',
		'CC-MAIN-2017-30',
		'CC-MAIN-2017-26',
		'CC-MAIN-2017-22',
		'CC-MAIN-2017-17',
		'CC-MAIN-2017-13',
		'CC-MAIN-2017-09',
		'CC-MAIN-2017-04'
	]
}

def getData(index):
	global links
	global out

	data = requests.get('http://index.commoncrawl.org/' + index + '-index?url=*.' + args.domain + '&output=json')
	data = data.text.split('\n')[:-1]

	for entry in data:
		link = json.loads(entry)['url']

		if link not in links:
			out = out + (link + '\n')


def crawlAll():
	for year, index in indexes.items():
		print('[!] Proceeding year: 20' + year[1:])

		for i in index:
			print('[-] ' + i)
			getData(i)


def crawlSpecific(year):
	index = indexes.get('y' + year)
	print('[!] Proceeding year: 20' + year)

	for i in index:
		print('[-] ' + i)
		getData(i)


if args.year:
	crawlSpecific(args.year)
else:
	crawlAll()

print('[-] Writing to file ...')
result.write(out)

print('[!] Done, file written: ./' + output)
