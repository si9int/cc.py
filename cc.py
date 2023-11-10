#!/usr/bin/env python3
import requests, json, os
import argparse, datetime, pathlib
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()

parser.add_argument('domain', help='domain which will be crawled for', type=str)
parser.add_argument('-y', '--year', help='limit the result to a specific year or range of years (default: all)', type=str)
parser.add_argument('-o', '--out', help='specify an output file (default: domain.txt)', type=str)
parser.add_argument('-l', '--list', help='Lists all available indexes', action='store_true')
parser.add_argument('-i', '--index', help='Crawl for a specific index (this will crawl all pages!)', type=str)
parser.add_argument('-u', '--update', help='Update index file', action='store_true')

args = parser.parse_args()
links = set()
out = ''
indexes = []

def getData(index, page):
    global links
    global out
    data = requests.get(f'http://index.commoncrawl.org/{index}-index?url=*.{args.domain}&output=json&page={page}')
    data = data.text.split('\n')[:-1]
    
    for entry in data:
        link = json.loads(entry)['url']

        if link not in links:
            links.add(link)
            out = out + (link + '\n')
            with open('./temp.tmp', 'a') as tmp_file:
                tmp_file.write(link + '\n')

def threadedCrawlIndex(index):
    print('[-] ' + index)
    url = f'http://index.commoncrawl.org/{index}-index?url=*.{args.domain}&output=json&showNumPages=true'
    data = requests.get(url).text
    try:
        pages = json.loads(data)['pages']
        print(f'[-] Collected {pages} pages')
        
        with ThreadPoolExecutor() as executor:
            executor.map(lambda x: getData(index, str(x)), range(pages))
    except:
        print('[!] Error reading index')
        pass

def readIndexFile(index_filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.txt")):
    global indexes
    path = pathlib.Path(index_filename)
    last_updated = datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d')
    print(f"Index file last updated on: {last_updated}. Run with -u to update.")
    
    with open(index_filename, "r") as f:
        indexes = f.read().split('\n')[:-1]

def updateIndexFile():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.txt"), "w") as f:
        url = "https://index.commoncrawl.org/collinfo.json"
        data = requests.get(url).text
        raw_indexes = json.loads(data)
        
        for index in raw_indexes:
            indexes.append(index['id'])
            f.write(index['id'] + "\n")

if args.update:
    updateIndexFile()
else:
    readIndexFile()

if args.list:
    for index in indexes:
        print('[-] ' + index)
else:
    years = args.year.split("-") if args.year else []
    if len(years) > 0:
        start_year, end_year = years[0], years[-1] if len(years) > 1 else years[0]
    else:
        start_year, end_year = None, None

    if args.index:
        threadedCrawlIndex(args.index)
    else:
        for index in indexes:
            year = index.split("-")[2]
            if args.year:
                if int(year) >= int(start_year) and int(year) <= int(end_year):
                    threadedCrawlIndex(index)
            else:
                threadedCrawlIndex(index)

if out:
    if args.out:
        path = os.path.abspath(args.out)
        result = open(path, 'w')
        output = str(args.out)
    else:
        result = open(f'./{args.domain}.txt', 'w')
        output = str(f'{args.domain}.txt')
    
    print('[-] Writing to file ...')
    result.write(out)
    os.remove('./temp.tmp')
    print(f'[!] Done, file written: ./{output}')
