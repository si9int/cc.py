# cc.py
Extracting URLs of a specific target based on the results of "commoncrawl.org"

**Usage**
```
cc.py [-h] domain

positional arguments:
  domain      domain which will be crawled for

optional arguments:
  -h, --help  show this help message and exit
```

**Example**
```
python3 cc.py github.com
cat github.com.txt | grep user
```

**Dependencies**
* Python3
