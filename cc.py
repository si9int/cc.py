#!/usr/bin/env python3
import requests, json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('domain', help = 'domain which will be crawled for', type = str)
parser.add_argument('-y', '--year', help = 'limit the result to a specific year (default: all)', type = str)
parser.add_argument('-o', '--out', help = 'specify an output file (default: domain.txt)', type = str)
parser.add_argument('-l', '--list', help = 'Lists all available indexes', action = 'store_true')
parser.add_argument('-i', '--index', help = 'Crawl for a specific index (this will crawl all pages!)', type = str)

args = parser.parse_args()
links = []
out = ''

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

def getData(index, page):
	global links
	global out

	data = requests.get('http://index.commoncrawl.org/' + index + '-index?url=*.' + args.domain + '&output=json&page=' + page)
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
			getData(i, '')


def crawlSpecific(year):
	index = indexes.get('y' + year)
	print('[!] Proceeding year: 20' + year)

	for i in index:
		print('[-] ' + i)
		getData(i, '')


def crawlIndex(domain, index):
	url = 'http://index.commoncrawl.org/' + index + '-index?url=*.' + domain + '&output=json&showNumPages=true'
	data = requests.get(url).text

	try:
		pages = json.loads(data)['pages']
		print('[-] Collected ' + str(pages) + ' pages')
	
		for i in range(0, pages):
			getData(index, str(i))
			print('[-] Proceeded page #' + str(i))
			
	except:
		print('[!] Error reading index')
		pass


if args.list:
	for year, index in indexes.items():
		for i in index:
			print('[-] ' + i)
else:
	if args.index:
		crawlIndex(args.domain, args.index)
	elif args.year:
		crawlSpecific(args.year)
	else:
		crawlAll()

if out:
	if args.out:
		result = open('./' + args.out, 'w')
		output = str(args.out)
	else:
		result = open('./' + args.domain + '.txt', 'w')
		output = str(args.domain + '.txt')

	print('[-] Writing to file ...')
	result.write(out)

	print('[!] Done, file written: ./' + output)
