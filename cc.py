import requests, json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('domain', help = 'domain which will be crawled for', type = str)

args = parser.parse_args()

indexes = [
	'CC-MAIN-2018-17',
	'CC-MAIN-2018-13',
	'CC-MAIN-2018-09',
	'CC-MAIN-2018-05',
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

output = []
result = open('./' + args.domain + '.txt', 'w')
links = []


for index in indexes:
	print('[-] Getting: ' + index)
	data = requests.get('http://index.commoncrawl.org/' + index + '-index?url=*.' + args.domain + '&output=json')
	data = data.text.split('\n')[:-1]
	output.append(data)

for entry in output:
	for link in entry:
		link = json.loads(link)['url']

		if link not in links:
			links.append(link + '\n')

print('[-] Writing URLS to file')

for link in links:
	result.write(link)

print('[!] Done, file written: ./' + args.domain + '.txt')
