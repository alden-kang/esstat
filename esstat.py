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

def getESStat(esRestSession, mode):

    if mode == "node" :
        response = esRestSession.request('GET',"/_nodes/stats")
        return json.loads(response.data)
    else :
        response = esRestSession.request('GET',"/_stats")
        return json.loads(response.data)

def printError(message):

    print "[ERROR] "+message

def printHeader(mode):

    if mode == "node":
        print "%20s\t%10s\t%10s\t%10s" % \
            ( "name","heap used ratio (%)","young gc time(ms)","old gc time(ms)" )
    else :
        print "%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s" % \
            ( "health","doc/s","time(ms)/doc","get/s","time(ms)/get","query/s","time(ms)/query","fetch/s","time(ms)/fetch" )

def printData(perfData, mode):

    if mode == "node":
        print "%20s\t%18.2f\t%18.2f\t%18.2f" % \
            (perfData['nodeName'], perfData['heapUsedRatio'], perfData['youngGCTime'], perfData['oldGCTime'])
    else :
        print "%10s\t%10s\t%12.2f\t%10s\t%12.2f\t%10s\t%12.2f\t%10s\t%12.2f" % \
            (perfData['clusterHealth'], perfData['indexTotalDiff'], perfData['indexTimeDiff'], perfData['getTotalDiff'], perfData['getTimeDiff'], perfData['queryTotalDiff'], perfData['queryTimeDiff'], perfData['fetchTotalDiff'], perfData['fetchTimeDiff'])

def monitoringNodeStatus(esRestSession, interval):

    # Inititialize variables

    line = 0

    perfData = dict()

    printHeader("node")

    statData = getESStat(esRestSession, "node")

    # Inititialize per node data dic
    for nodeID in statData['nodes']:

        nodeStat = statData['nodes'][nodeID]
        nodeName = nodeStat['name']

        perfData[nodeName] = dict()
        perfData[nodeName]['havingPrevData'] = False

    while(True):

        statData = getESStat(esRestSession, "node")

        for nodeID in statData['nodes']:

            nodeStat = statData['nodes'][nodeID]
            nodeName = nodeStat['name']

            perfData[nodeName]['nodeName'] = nodeName

            # Get Heap Memory Usage
            heapUsedPercentCurr = nodeStat['jvm']['mem']['heap_used_percent']

            # Get Young GC Time
            perfData[nodeName]['youngGCCountCurr'] = nodeStat['jvm']['gc']['collectors']['young']['collection_count']
            perfData[nodeName]['youngGCTimeCurr'] = nodeStat['jvm']['gc']['collectors']['young']['collection_time_in_millis']

            # Get Old GC Time
            perfData[nodeName]['oldGCCountCurr'] = nodeStat['jvm']['gc']['collectors']['old']['collection_count']
            perfData[nodeName]['oldGCTimeCurr'] = nodeStat['jvm']['gc']['collectors']['old']['collection_time_in_millis']

            #print "[DEBUG] " + nodeName + " : " + str(youngGCCountCurr) + " , " + str(youngGCTimeCurr)

            if perfData[nodeName]['havingPrevData'] == True :

                perfData[nodeName]['heapUsedRatio'] = heapUsedPercentCurr

                try:
                    perfData[nodeName]['youngGCTime'] = (perfData[nodeName]['youngGCTimeCurr'] - perfData[nodeName]['youngGCTimePrev']) \
                                                        / (perfData[nodeName]['youngGCCountCurr'] - perfData[nodeName]['youngGCCountPrev'])
                except:
                    perfData[nodeName]['youngGCTime'] = 0.0

                try:
                    perfData[nodeName]['oldGCTime'] = (perfData[nodeName]['oldGCTimeCurr'] - perfData[nodeName]['oldGCTimePrev']) \
                                                        / (perfData[nodeName]['oldGCCountCurr'] - perfData[nodeName]['oldGCCountPrev'])
                except:
                    perfData[nodeName]['oldGCTime'] = 0.0

                printData(perfData[nodeName], "node")

            perfData[nodeName]['youngGCCountPrev'] = perfData[nodeName]['youngGCCountCurr']
            perfData[nodeName]['youngGCTimePrev'] = perfData[nodeName]['youngGCTimeCurr']

            perfData[nodeName]['oldGCCountPrev'] = perfData[nodeName]['oldGCCountCurr']
            perfData[nodeName]['oldGCTimePrev'] = perfData[nodeName]['oldGCTimeCurr']

            perfData[nodeName]['havingPrevData'] = True

        line = line+1
        print ""
        if line%10 == 0 :
            printHeader("node")
        time.sleep(interval)


def monitoringClusterStatus(esRestSession, interval):

    # Inititialize variables

    line = 0

    perfData = {}

    havingPrevData = False

    printHeader("cluster")

    while(True):

        perfData['clusterHealth'] = getESStatus(esRestSession)
        statData = getESStat(esRestSession, "cluster")

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

            perfData['indexTotalDiff'] = (indexTotalCurr - indexTotalPrev) / interval
            try:
                perfData['indexTimeDiff'] = float(indexTimeCurr - indexTimePrev) / float(perfData['indexTotalDiff'])
            except:
                perfData['indexTimeDiff'] = 0.0

            perfData['getTotalDiff'] = (getTotalCurr - getTotalPrev) / interval
            try:
                perfData['getTimeDiff'] = float(getTimeCurr - getTimePrev) / float(perfData['getTotalDiff'])
            except:
                perfData['getTimeDiff'] = 0.0

            perfData['queryTotalDiff'] = (queryTotalCurr - queryTotalPrev) / interval
            try:
                perfData['queryTimeDiff'] = float(queryTimeCurr - queryTimePrev) / float(perfData['queryTotalDiff'])
            except:
                perfData['queryTimeDiff'] = 0.0

            perfData['fetchTotalDiff'] = (fetchTotalCurr - fetchTotalPrev) / interval
            try:
                perfData['fetchTimeDiff'] = float(fetchTimeCurr - fetchTimePrev) / float(perfData['fetchTotalDiff'])
            except:
                perfData['fetchTimeDiff'] = 0.0

            perfData['mergeTotalDiff'] = (mergeTotalCurr - mergeTotalPrev) / interval
            try:
                perfData['mergeTimeDiff'] = float(mergeTimeCurr - mergeTimePrev) / float(perfData['mergeTotalDiff'])
            except:
                perfData['mergeTimeDiff'] = 0.0

            perfData['refreshTotalDiff'] = (refreshTotalCurr - refreshTotalPrev) / interval
            try:
                perfData['refreshTimeDiff'] = float(refreshTimeCurr - refreshTimePrev) / float(perfData['refreshTotalDiff'])
            except:
                perfData['refreshTimeDiff'] = 0.0

            perfData['flushTotalDiff'] = (flushTotalCurr - flushTotalPrev) / interval
            try:
                perfData['flushTimeDiff'] = float(flushTimeCurr - flushTimePrev) / float(perfData['flushTotalDiff'])
            except:
                perfData['flushTimeDiff'] = 0.0

            if line%10 == 0 :
                print "\n"
                printHeader("cluster")
            printData(perfData, "cluster")

        line = line+1
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

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", help="monitoring mode , cluster is cluster health and tps , node is node health and gc infomation (default cluster)",default="cluster", required=False)
    parser.add_argument("--url", help="the url of cluster (default localhost)",default="localhost", required=False)
    parser.add_argument("--port", help="the port of cluster (default 9200)", default=9200, required=False)
    parser.add_argument("--interval", help="the interval of stat api request (default 1s)", default=1, required=False, type=int)

    args = parser.parse_args()

    mode = args.mode
    url = args.url
    port = args.port
    interval = args.interval

    try:

        esRestSession = urllib3.HTTPConnectionPool(url, maxsize=1, port=port, timeout=10)
        esRestSession.request('GET', '/')

    except:

        printError("ElasticSearch is not installed on " + url + ":" + str(port))
        exit(1)



    if mode == "node":
        monitoringNodeStatus(esRestSession, interval)

    else :
        monitoringClusterStatus(esRestSession, interval)



if __name__ == "__main__":
    main()
