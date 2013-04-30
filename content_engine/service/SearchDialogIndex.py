#!/usr/local/bin/python2.7
#coding: utf-8

import sys, struct, os, logging, traceback, heapq
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)
import leveldb
from SegUtil import SegUtil
from BuildDialogIndex import DBItem, Index

from weixin.models import BaseDialog
from search_pb2 import Query, ResponseDialog, QueryTerm, RelatedDialog


from Utils import *

workPath = os.path.dirname(os.path.abspath(__file__))

class HitList:
    def __init__(self):
        """
        every item is (qId, weight)
        """
        self.hitList = []

class SearchIndex:
    def __init__(self, dataPath, segPath):
        self.dataPath = dataPath
        self.segPath = segPath
        options = {
            'create_if_missing': True,
            'error_if_exists': False,
            'paranoid_checks': False,
            'block_cache_size': 100 * (1 << 20),
            'write_buffer_size': 2 * (1 << 20),
            'block_size': 4096,
            'max_open_files': 1000,
            'block_restart_interval': 16
        }
        self.db = leveldb.LevelDB(self.dataPath, **options)
        self.logger = logging.getLogger("search")


    def GetHitList(self, term):
        term = term.lower()
        self.logger.debug("get hit list for %s" % term)
        startItem = DBItem(term, 0, 0)
        endItem = DBItem(term, 0xFFFFFFFF, 0)
        startKey = startItem.EncodeKey()
        endKey = endItem.EncodeKey()
        hitList = HitList()

        for k, v in self.db.RangeIter(key_from = startKey, key_to = endKey):
            item = DBItem("", 0, 0)
            item.Decode(k, v)
            self.logger.debug("get qId %d weight %f" % (item.qId, item.weight))

            hitList.hitList.append((item.qId, item.weight))
        return hitList

    def Search(self, query):
        terms = Index.GetWords(query)
        hitListList = []
        curIndex = []

        for term in terms:
            term = term[0]
            self.logger.debug("term %s" % term)
            hitList = self.GetHitList(term)
            hitListList.append(hitList)
            curIndex.append(0)


        maxWeight = 0
        maxQId = -1
        while True:
            tmpWeight = 0
            curMinQId = 0xFFFFFFFF
            for i in range(len(hitListList)):
                if curIndex[i] < len(hitListList[i].hitList) and hitListList[i].hitList[curIndex[i]][0] < curMinQId:
                    curMinQId = hitListList[i].hitList[curIndex[i]][0]
            if curMinQId == 0xFFFFFFFF:
                break

            self.logger.debug("deal with qId %d" % curMinQId)
            for i in range(len(hitListList)):
                if curIndex[i] < len(hitListList[i].hitList) and hitListList[i].hitList[curIndex[i]][0] == curMinQId:
                    tmpWeight += hitListList[i].hitList[curIndex[i]][1]
                    curIndex[i] += 1

            if tmpWeight > maxWeight:
                maxWeight = tmpWeight
                maxQId = curMinQId

        return ([(maxQId, maxWeight),], terms)

    def RespQuery(self, result, dialogs, terms, address, s):
        resp = ResponseDialog()
        resp.result = result
        for t in terms:
            q = resp.terms.add()
            q.term = t[0]
            q.weight = t[1]

        for d in dialogs:
            q = resp.dialogs.add()
            q.qId = d[0] 
            q.rel = d[1]
        s.sendto(resp.SerializeToString(), address)

    def InitSeg(self):
        SegUtil.Init(self.segPath)
       
    def StartServer(self, port):
        import socket
        host = '127.0.0.1'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind( (host, port) )

        while True:
            try:
                message, address = s.recvfrom(8192)
                self.logger.debug("len %d" % len(message))
                query = Query()
                try:
                    query.ParseFromString(message)
                except:
                    self.logger.debug(traceback.format_exc())
                    self.RespQuery(1, 0, 0, [], address, s)
                    continue
                self.logger.debug("get content %s" % query.query)
                dialogs, terms = self.Search(query.query)
                for d in dialogs:
                    self.logger.debug("dialog %d weight %f" % (d[0], d[1]))

                for t in terms:
                    self.logger.debug(" terms %s" % t[0])

                self.RespQuery(0, dialogs, terms, address, s)
            except KeyboardInterrupt:
                break
            except:
                self.logger.error(traceback.format_exc())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s cfg" % sys.argv[0]
        sys.exit()

    os.chdir(workPath)
    port = int(GetConfigValue("SEARCH_PORT", sys.argv[1]))
    pidFileName = GetConfigValue("PID_FILE", sys.argv[1])
    print port, pidFileName
    pidFile = file(pidFileName, "w")
    pidFile.write("%d" % os.getpid())
    pidFile.close()

    dbPath = GetConfigValue("DB_PATH", sys.argv[1])
    search = SearchIndex(dbPath, workPath + "/../")
    search.InitSeg()
    search.StartServer(port)


