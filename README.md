# cc.py
Extracting URLs of a specific target based on the results of "commoncrawl.org".  
Updated to v.0.3 | Whats new:

- 65% faster proceeding
- Specify a year via `-y/--year`, e.g.: `-y 2018`
- Specify an output file via `-o/--out`, e.g.: `-o whatever.txt`
- Crawl all pages for a specific index `-i/--index`, e.g.: `cc.py army.mil -i CC-MAIN-2018-05`
- List all available indexes `-l/--list`, e.g.: `cc.py army.mil -l`


**ToDo**

- [x] Crawl for a specific index
- [x] Implementation of multithreading
- [x] Allowing a range of years as input
- [ ] Implementing `direct-grep`
- [x] Temporary file-writing 

**Usage**
```
cc.py [-h] [-y YEAR] [-o OUT] [-l] [-i INDEX] [-u] domain

positional arguments:
  domain                domain which will be crawled for

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  limit the result to a specific year (default: all)
  -o OUT, --out OUT     specify an output file (default: domain.txt)
  -l, --list            Lists all available indexes
  -i INDEX, --index INDEX
                        Crawl for a specific index (this will crawl all
                        pages!)
  -u, --update          Update index file

```

**Example**
```
python3 cc.py github.com -y 2018 -o github_18.txt
cat github_18.txt | grep user
```

**Dependencies**
* Python3

> This is a fork from the main repository, i just added some missing features
