#!/usr/bin/env python
# coding: utf8

import sys

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, Python 3.x is required\n")
    sys.exit(1)

import json
import os
import argparse
import requests

def main():
    domain, outfile, index_used = getArguments()

    work_path = os.path.dirname(os.path.realpath(__file__))
    indices = getIndices(work_path)
    indices = filterIndices(index_used, indices)

    ccEntries = []

    for index in indices:
        print("\033[32m[i]\033[0m Request to {}".format(index))

        url = makeCCUrl(domain, index)

        try:
            lines = getCCResponse(url)
            ccEntries.append(lines)

        except Exception as e:
            print("\033[31m[?!]\033[0m Request excpetion [FYI!]")
            print(e)

    print("\033[32m[i] Finished all requests \033[0m")
    print("Found {} lines in responses".format(len(ccEntries)))

    print("Extracting links...")
    links = extractLinksFromCC(ccEntries)

    print("Writing links to {}".format(outfile))
    writeResults(links, outfile)

    print("Finished!")


def writeResults(links, outfile):
    fw = open(outfile, "w")
    for link in links:
        fw.write(link)


def extractLinksFromCC(ccEntries):
    links = []
    for entry in ccEntries:
        for link in entry:
            link = json.loads(link)["url"]

            if link not in links:
                links.append(link + "\n")

    return links


def getCCResponse(url):
    response = requests.get(url, verify=False, timeout=10, allow_redirects=True)
    return response.text.split("\n")[:-1]


def makeCCUrl(domain, index):
    url = "http://index.commoncrawl.org/" + index + "-index?url=*." + domain + "&output=json".format()
    return url


def filterIndices(index_used, indices):

    if index_used is not None:
        indices = intersectLists(indices, index_used)

    if len(indices) == 0:
        print("\033[31m[!] Not indices selected, may your filter is wrong!\033[0m")
        sys.exit()

    return indices


def intersectLists(indices, index_used_list):
    lst3 = [value for value in indices if value in index_used_list]
    return lst3


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--domain",
        help="domain",
        type=str,
        dest="domain",
        default=None,
        required=True
    )
    parser.add_argument(
        "-o", "--outfile",
        help="Path to save the output",
        type=str,
        dest="outfile",
        required=True

    )
    parser.add_argument(
        "-i", "--index",
        nargs="?",
        type=str,
        action="append",
        help="Use only this index",
        dest="index_used",
        default=None
    )
    args = parser.parse_args()

    return args.domain, args.outfile, args.index_used


def getIndices(work_path):
    indices_path = os.path.join(work_path, "indices.json")
    with open(indices_path) as f:
        data = json.load(f)
    indexlist = []
    for element in data:
        indexlist.append(element["index"])

    return indexlist


if __name__ == "__main__":
    main()
