#!/usr/local/bin/python2.7
#coding: utf-8

import sys, struct, os, logging
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)
import leveldb, PySeg
from BuildIndex import DBItem
workPath = os.path.dirname(os.path.abspath(__file__))
NameAddr = 1
CategoryAddr = 2
TagAddr = 3
DescAddr = 4

class HitList:
    def __init__(self):
        self.hitList = []

class SearchIndex:
    def __init__(self, dataPath, segPath):
        self.dataPath = dataPath
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
        PySeg.init(segPath)


    def GetHitList(self, term):
        self.logger.debug("get hit list for %s" % term.decode("utf8"))
        startKey = struct.pack("!H%dsI" % len(term), len(term), term, 0)
        endKey = struct.pack("!H%dsI" % len(term), len(term), term, 0xFFFFFFFF)
        hitList = HitList()
        for k, v in self.db.RangeIter(key_from = startKey, key_to = endKey):
            item = DBItem("", 0, [])
            item.Decode(k, v)
            self.logger.debug("get gameId %d addrs %s" % (item.gameId, str(item.addrs)))
            hitList.hitList.append((item.gameId, item.addrs))
        return hitList


    def Search(self, query):
        terms = PySeg.seg(query)
        hitListList = []
        for term in terms:
            hitList = self.GetHitList(term)
        hitListList.append(hitList)

        termWeight = []
        curAddr = []
        allNum = 0
        addrWeight = {NameAddr:0.2, CategoryAddr:0.3, TagAddr:0.4, DescAddr:0.1}
        for i in range(len(hitListList)):
            allNum += len(hitListList[i].hitList)
            termWeight.append(len(hitListList[i].hitList))
            curAddr.append(0)
        for i in range(len(hitListList)):
            termWeight[i] = termWeight[i] / allNum


        maxWeight = 0
        maxGameId = 0
        while True:
            curMinGameId = 0xFFFFFFFF
            for i in range(len(hitListList)):
                if curAddr[i] < len(hitListList[i].hitList) and hitListList[i].hitList[curAddr[i]][0] < curMinGameId:
                    curMinGameId = hitListList[i].hitList[curAddr[i]][0]
            if curMinGameId == 0xFFFFFFFF:
                break
            self.logger.debug("deal with gameId %d" % curMinGameId)
            curWeight = 0
            for i in range(len(hitListList)):
                if hitListList[i].hitList[curAddr[i]][0] == curMinGameId:
                    for addr in hitListList[i].hitList[curAddr[i]][1]:
                        curWeight += termWeight[i] * addrWeight[addr]
                    self.logger.debug("hit term %d %f" % (i, curWeight))
                    curAddr[i] += 1
            if curWeight > maxWeight:
                maxWeight = curWeight
                maxGameId = curMinGameId


        self.logger.debug("max game id %d %f" % (maxGameId, maxWeight))
        return maxGameId


if __name__ == "__main__":
    search = SearchIndex(workPath + "/../db/", workPath + "/../")

    print search.Search("僵尸")


