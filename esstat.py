#!/usr/local/python

import argparse
import json
import urllib3
import time

def getESStatus(esRestSession):

    response = esRestSession.request('GET',"/_cat/health")
    if response.data.find("green") :
        return "green"
    elif response.data.find("yellow") :
        return "yellow"
    else :
        return "red"

def getESStat(esRestSession):

    response = esRestSession.request('GET',"/_stats?pretty")
    return json.loads(response.data)

def printError(message):

    print "[ERROR] "+message

def printHeader():

    print "%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s" % \
        ( "health","doc/s","time/doc","get/s","time/get","query/s","time/query","fetch/s","time/fetch" )

def printData(perfData):

    print "%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s" % \
        (perfData['clusterHealth'], perfData['indexTotalDiff'], perfData['indexTimeDiff'], perfData['getTotalDiff'], perfData['getTimeDiff'], perfData['queryTotalDiff'], perfData['queryTimeDiff'], perfData['fetchTotalDiff'], perfData['fetchTimeDiff'])

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--url", help="the url of cluster (default localhost)",default="localhost", required=False)
    parser.add_argument("--port", help="the port of cluster (default 9200)", default=9200, required=False)
    parser.add_argument("--interval", help="the interval of stat api request (default 1s)", default=1, required=False)

    args = parser.parse_args()

    url = args.url
    port = args.port
    interval = args.interval

    try:

        esRestSession = urllib3.HTTPConnectionPool(url, maxsize=1, port=port, timeout=10)
        esRestSession.request('GET', '/')

    except:

        printError("ElasticSearch is not installed on " + url + ":" + str(port))
        exit(1)

    # Inititialize variables

    perfData = {}

    havingPrevData = False

    printHeader()

    while(True):

        perfData['clusterHealth'] = getESStatus(esRestSession)
        statData = getESStat(esRestSession)

        # Get indexing performance

        indexTotalCurr = statData["_all"]["primaries"]["indexing"]["index_total"]
        indexTimeCurr = statData["_all"]["primaries"]["indexing"]["index_time_in_millis"]

        # Get get performance

        getTotalCurr = statData["_all"]["primaries"]["get"]["total"]
        getTimeCurr = statData["_all"]["primaries"]["get"]["time_in_millis"]

        # Get search performance

        queryTotalCurr = statData["_all"]["primaries"]["search"]["query_total"]
        queryTimeCurr = statData["_all"]["primaries"]["search"]["query_time_in_millis"]
        fetchTotalCurr = statData["_all"]["primaries"]["search"]["fetch_total"]
        fetchTimeCurr = statData["_all"]["primaries"]["search"]["fetch_time_in_millis"]

        # Get merge performance

        mergeTotalCurr = statData["_all"]["primaries"]["merges"]["total"]
        mergeTimeCurr = statData["_all"]["primaries"]["merges"]["total_time_in_millis"]

        # Get refresh performance

        refreshTotalCurr = statData["_all"]["primaries"]["refresh"]["total"]
        refreshTimeCurr = statData["_all"]["primaries"]["refresh"]["total_time_in_millis"]

        # Get Flush performance

        flushTotalCurr = statData["_all"]["primaries"]["flush"]["total"]
        flushTimeCurr = statData["_all"]["primaries"]["flush"]["total_time_in_millis"]

        if havingPrevData == True :

            perfData['indexTotalDiff'] = indexTotalCurr - indexTotalPrev
            perfData['indexTimeDiff'] = indexTimeCurr - indexTimePrev
            perfData['getTotalDiff'] = getTotalCurr - getTotalPrev
            perfData['getTimeDiff'] = getTimeCurr - getTimePrev
            perfData['queryTotalDiff'] = queryTotalCurr - queryTotalPrev
            perfData['queryTimeDiff'] = queryTimeCurr - queryTimePrev
            perfData['fetchTotalDiff'] = fetchTotalCurr - fetchTotalPrev
            perfData['fetchTimeDiff'] = fetchTimeCurr - fetchTimePrev
            perfData['mergeTotalDiff'] = mergeTotalCurr - mergeTotalPrev
            perfData['mergeTimeDiff'] = mergeTimeCurr - mergeTimePrev
            perfData['refreshTotalDiff'] = refreshTotalCurr - refreshTotalPrev
            perfData['refreshTimeDiff'] = refreshTimeCurr - refreshTimePrev
            perfData['flushTotalDiff'] = flushTotalCurr - flushTotalPrev
            perfData['flushTimeDiff'] = flushTimeCurr - flushTimePrev

            printData(perfData)

        indexTotalPrev = indexTotalCurr
        indexTimePrev = indexTimeCurr
        getTotalPrev = getTotalCurr
        getTimePrev = getTimeCurr
        queryTotalPrev = queryTotalCurr
        queryTimePrev = queryTimeCurr
        fetchTotalPrev = fetchTotalCurr
        fetchTimePrev = fetchTimeCurr
        mergeTotalPrev = mergeTotalCurr
        mergeTimePrev = mergeTimeCurr
        refreshTotalPrev = refreshTotalCurr
        refreshTimePrev = refreshTimeCurr
        flushTotalPrev = flushTotalCurr
        flushTimePrev = flushTimeCurr

        havingPrevData = True

        time.sleep(interval)

if __name__ == "__main__":
    main()
