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
  --mode MODE          monitoring mode , cluster is cluster health and tps , node is node health and gc infomation (default cluster)
```

## Example

1) Cluster Mode
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

2) Node Mode
```
[root@server ~]# python ./esstat.py --mode node
                name	heap used ratio (%)	young gc time(ms)	old gc time(ms)

 search-node03	             72.00	              0.00	              0.00
 search-node01	             25.00	              0.00	              0.00
 search-node02	             53.00	              0.00	              0.00
 search-node04	             79.00	              0.00	              0.00
 search-node05	             26.00	              0.00	              0.00

 search-node03	             73.00	              0.00	              0.00
 search-node01	             21.00	             43.00	              0.00
 search-node02	             49.00	             36.00	              0.00
 search-node04	             81.00	              0.00	              0.00
 search-node05	             22.00	             32.00	              0.00
 ```

## Changelog

See the [CHANGELOG.md file](CHANGELOG.md).
