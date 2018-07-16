# cc.py
Extracting URLs of a specific target based on the results of "commoncrawl.org".  
Updated to v.0.2 | Whats new:

- 65% faster proceeding
- Specify a year via `-y/--year`, e.g.: `-y 18`
- Specify an output file via `-o/--out`, e.g.: `-o whatever.txt`

**ToDo**

- [ ] Implementation of multi-threating
- [ ] Allowing a range of years as input
- [ ] Implementing `direct-grep`
- [ ] Temporary file-writing 

**Usage**
```
cc.py [-h] [-y YEAR] [-o OUT] domain

positional arguments:
  domain                domain which will be crawled for

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  limit the result to a specific year (default: all)
  -o OUT, --out OUT     specify an output file (default: domain.txt)
```

**Example**
```
python3 cc.py github.com -y 18 -o github_18.txt
cat github_18.txt | grep user
```

**Dependencies**
* Python3
