#!/usr/bin/env python3
import requests, json, os
import argparse, datetime, pathlib

parser = argparse.ArgumentParser()

parser.add_argument('domain', help = 'domain which will be crawled for', type = str)
parser.add_argument('-y', '--year', help = 'limit the result to a specific year (default: all)', type = str)
parser.add_argument('-o', '--out', help = 'specify an output file (default: domain.txt)', type = str)
parser.add_argument('-l', '--list', help = 'Lists all available indexes', action = 'store_true')
parser.add_argument('-i', '--index', help = 'Crawl for a specific index (this will crawl all pages!)', type = str)
parser.add_argument('-u', '--update', help = 'Update index file', action = 'store_true')

args = parser.parse_args()
links = []
out = ''

indexes = []

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
	#Below code assumes that array is sorted
	#Reverse sort ensures that most recent years are prioritised, not essential. 
	currentyear=0
	indexes.sort(reverse=1)
	
	for index in indexes:
		if currentyear != index.split("-")[2]:
			currentyear = index.split("-")[2]
			print("[!] Processing year: " + currentyear)
		print('[-] ' + index)
		getData(index, '')

#
def crawlSpecific(domain, year):
	#index = indexes.get('y' + year)
	print('[!] Processing year: ' + year)

	for index in indexes:
		if year in index:
			print('[-] ' + index)
			crawlIndex(domain, index)


def crawlIndex(domain, index):
	url = 'http://index.commoncrawl.org/' + index + '-index?url=*.' + domain + '&output=json&showNumPages=true'
	data = requests.get(url).text
	try:
		pages = json.loads(data)['pages']
		print('[-] Collected ' + str(pages) + ' pages')
	
		for i in range(0, pages):
			getData(index, str(i))
			print('[-] Processing page #' + str(i))
			
	except:
		print('[!] Error reading index')
		pass

def readIndexFile(index_filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.txt")):
	global indexes
	#check when the index file was last updated
	path = pathlib.Path(index_filename)
	last_updated=datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d')
	print("Index file last updated on:", last_updated, "run with -u to update.")

	with open(index_filename, "r") as f:
		indexes = f.read().split('\n')[:-1]

def updateIndexFile():
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.txt"), "w") as f:
		url = "https://index.commoncrawl.org/collinfo.json"
		data = requests.get(url).text
		raw_indexes = json.loads(data)
		for index in raw_indexes:
			indexes.append(index['id'])
			f.write(index['id']+"\n")


#check if we need to update the index file or just read it into the array

if args.update:
	updateIndexFile()
else:
	readIndexFile()

if args.list:
	for index in indexes:
		print('[-] ' + index)	
else:
	if args.index:
		crawlIndex(args.domain, args.index)
	elif args.year:
		crawlSpecific(args.domain, args.year)
	else:
		crawlAll()

if out:
	if args.out:
		path = os.path.abspath(args.out)
		result = open(path, 'w')
		output = str(args.out)
	else:
		result = open('./' + args.domain + '.txt', 'w')
		output = str(args.domain + '.txt')

	print('[-] Writing to file ...')
	result.write(out)

	print('[!] Done, file written: ./' + output)
