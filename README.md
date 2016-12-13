# ElasticSearch Status Tool

## About

You can see stats of elasticsearch cluster like vmstat tool.
It shows cluster health, documents per seconds, etc.

## Requirements
- python
- python urllib3

## Features
- documents per second : doc/s
- indexing time per document : time/doc
- get requests per second : get/s
- latency per get request : time/get
- query requests per second : query/s
- latency per query request : time/query
- fetch requests per second : fetch/s
- latency per fetch request : time/fetch

## Usage
```
usage: esstat.py [-h] [--url URL] [--port PORT] [--interval INTERVAL]

optional arguments:
  -h, --help           show this help message and exit
  --url URL            the url of cluster (default localhost)
  --port PORT          the port of cluster (default 9200)
  --interval INTERVAL  the interval of stat api request (default 1s)
```

## Example
```
[root@server ~]# python ./esstat.py
    health	     doc/s	  time/doc	     get/s	  time/get	   query/s	time/query	   fetch/s	time/fetch
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         1	         1	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	      2523	       190	         0	         0	         0	         0	         0	         0
     green	       173	        24	         0	         0	         0	         0	         0	         0
     green	        47	        23	         0	         0	         0	         0	         0	         0
     green	         3	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         1	         1	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	      2424	       168	         0	         0	         0	         0	         0	         0
     green	        32	         2	         0	         0	         0	         0	         0	         0
     green	         1	         1	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
     green	         0	         0	         0	         0	         0	         0	         0	         0
```

## Changelog

See the [CHANGELOG.md file](CHANGELOG.md).
