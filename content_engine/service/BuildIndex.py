#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*-

import sys, subprocess, os, os.path
workPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(workPath + "/..")
from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

from portal.models import Game, Category
import leveldb
from SegUtil import SegUtil
import logging, struct, os, os.path
from taggit.models import Tag

from Utils import *
NameAddr = 1
CategoryAddr = 2
TagAddr = 3
DescAddr = 4
logger = logging.getLogger("build_index")
single = workPath + "/update_index.single"


class DBItem:
    def __init__(self, term, gameId, addrs):
        self.term = term
        self.gameId = gameId
        self.addrs = addrs
        self.nameWeight = 0

    def Encode(self):
        term = self.term.encode("utf8")
        key = struct.pack("!H%dsI" % len(term), len(term), term, self.gameId)
        value = struct.pack("!B%dB" % len(self.addrs), len(self.addrs), *self.addrs)
        value += struct.pack("!I", int(self.nameWeight * 100000))
        return (key, value)

    def EncodeKey(self):
        term = self.term.encode("utf8")
        key = struct.pack("!H%dsI" % len(term), len(term), term, self.gameId)
        return key
        
    def Decode(self, key, value):
        start = 0
        wLen = struct.unpack("!H", key[start: start + 2])[0]
        start += 2
        self.term = key[start: start + wLen].decode("utf8")
        start += wLen
        self.gameId = struct.unpack("!I", key[start: start + 4])[0]

        start = 0
        cLen = struct.unpack("!B", value[start: start + 1])[0]
        start += 1
        self.addrs = struct.unpack("!%dB" % cLen, value[start:start + cLen])
        start += cLen
        self.nameWeight = struct.unpack("!I", value[start:start + 4])[0]
        self.nameWeight /= 100000.0;

class Index:
    def __init__(self, dataPath):
        self.path = dataPath

    def Show(self):
        item = DBItem("", 0, [])
        for k,v in self.db.RangeIter(include_value = True):
            item.Decode(k, v)
            self.logger.debug("term %s gameId %d addrs %s nameWeight %f" % (item.term, item.gameId, str(item.addrs), item.nameWeight))


    def CreateDB(self):
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
        self.db = leveldb.LevelDB(self.path, **options)
        self.logger = logging.getLogger("build_index") 
        SegUtil.Init(self.path + "/../")


    @classmethod
    def RightPos(cls, pos):
        if len(pos) == 0 or pos[0] == 'w':
            return False 
        else:
            return True


    @classmethod
    def GetRightWords(cls, sentenses, logger = None):
        words = {}
        allWeight = 0
        for s in sentenses:
            ts = SegUtil.Seg(s.encode('utf8'))
            for t in ts:
                if cls.RightPos(t[1]):
                    if logger:
                        logger.debug("%s pos %s" % (t[0], t[1]))
                    if t[1][0] == 'v' or t[1][0] == 'n':
                        weight = 3
                    elif t[1] == 'a':
                        weight = 1.5
                    else:
                        weight = 1
                    allWeight += weight
                    if t[0].decode('utf8') not in words:
                        words[t[0].decode('utf8')] = 0
                    words[t[0].decode('utf8')] += weight
        res = []
        for k,v in words.items():
            res.append((k, float(v) / allWeight))
        res.sort(key=lambda g:g[1], reverse=True)
        return res

    @classmethod    
    def BuildIndexForOne(cls, db, logger, gameId, name, description, categorys, tags):
        terms = {}
        logger.debug("build index for one %d %s %s %s %s" % (gameId, name, description, str(categorys), str(tags)))
        ts = cls.GetRightWords([name,], logger)
        terms[NameAddr] = []
        term2NameWeight = {}
        for t in ts:
            terms[NameAddr].append(t[0])
            logger.debug("%s weight %f" % (t[0], t[1]))
            term2NameWeight[t[0]] = t[1]
        ts = cls.GetRightWords([description,])
        terms[DescAddr] = []
        for t in ts:
            terms[DescAddr].append(t[0])

        terms[CategoryAddr] = []
        ts = cls.GetRightWords(categorys)
        for t in ts:
            terms[CategoryAddr].append(t[0])
        ts = cls.GetRightWords(tags)
        terms[TagAddr] = []
        for t in ts:
            terms[TagAddr].append(t[0])
        term2Addrs = {}

        for k, v in terms.items():
            for term in v:
                if term not in term2Addrs:
                    term2Addrs[term] = []

                if k not in term2Addrs[term]:
                    term2Addrs[term].append(k)


        logger.debug("name weight %s", str(term2NameWeight))
        for term, addrs in term2Addrs.items():
            item = DBItem(term, gameId, addrs)
            if term in term2NameWeight:
                item.nameWeight = term2NameWeight[term]
            else:
                item.nameWeight = 0
            logger.debug("term %s addrs %s nameWeight %f" % (term, str(addrs), item.nameWeight))
            (k, v) = item.Encode()

            db.Put(k, v)

if __name__ == "__main__":
    os.chdir(workPath)
    if len(sys.argv) != 2:
        print "Usage: %s cfg" % sys.argv[0]
        sys.exit()

    if not CheckSingle(single):
        logger.error("another instance is running")
        sys.exit()

    dbPath = GetConfigValue("DB_PATH", sys.argv[1])
    if dbPath[-1] == '/':
        dbPath = dbPath[:-1]
    if CheckFileExist(dbPath + ".tmp"):
        DeleteFolders(dbPath + ".tmp")
    index = Index(dbPath + ".tmp")
    index.CreateDB()
    games = Game.objects.all()
    for game in games:
        tags = []
        for t in game.tags.all():
            tags.append(t.name)
        cats = [game.category.name, ]
        index.BuildIndexForOne(index.db, index.logger, game.pk, game.name, game.description, cats, tags)


    pidFilePath = GetConfigValue("PID_FILE", sys.argv[1])
    port = int(GetConfigValue("SEARCH_PORT", sys.argv[1]))
    logger.debug("%s %d" % (pidFilePath, port))
    if CheckFileExist(pidFilePath) and PortIsUsed(port):
        logger.debug("search index active")
        pidFile = file(pidFilePath)
        pid = int(pidFile.readline().strip())
        KillOne(pid)
        pidFile.close()
    else:
        logger.debug("search index not active")

    if CheckFileExist(dbPath + ".bak"):
        DeleteFolders(dbPath + ".bak")
    if CheckFileExist(dbPath):
        os.rename(dbPath, dbPath + ".bak")
        DeleteFolders(dbPath)
    os.rename(dbPath + ".tmp", dbPath)

    subprocess.Popen("./SearchIndex.py Search.cfg", shell=True)
    RemoveSingle(single)



