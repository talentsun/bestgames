#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*-

import sys, subprocess, os
workPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(workPath + "/..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)
from weixin.models import BaseDialog
import leveldb
from SegUtil import SegUtil
import logging

from Utils import *

logger = logging.getLogger("build_index")
single = workPath + "/build_dialog_index.single"

class DBItem:
    def __init__(self, term, qId, weight):
        self.term = term
        self.qId = qId
        self.weight = weight


    def Encode(self):
        term = self.term.encode("utf8")
        key = struct.pack("!H%dsI" % len(term), len(term), term, self.qId)

        value = struct.pack("!I", int(self.weight * 10000))

        return (key, value)


    def EncodeKey(self):
        term = self.term.encode("utf8")
        key = struct.pack("!H%dsI" % len(term), len(term), term, self.qId)
        return key


    def Decode(self, key, value):
        start = 0
        wLen = struct.unpack("!H", key[start: start + 2])[0]
        start += 2
        self.term = key[start : start + wLen].decode("utf8")
        start += wLen
        self.qId = struct.unpack("!I", key[start : start + 4])[0]

        start = 0
        self.weight = struct.unpack("!I", value[start:start + 4])[0]
        self.weight /= 10000.0

class Index:
    def __init__(self, dataPath):
        self.path = dataPath


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
        SegUtil.Init(workPath + "/../")

    @classmethod
    def GetWords(cls, sentense, logger = None):
        ts = SegUtil.Seg(sentense.encode("utf8"))
        unique_word = {}
        for t in ts:
            if not t[0] in unique_word:
                unique_word[t[0]] = 0
            unique_word[t[0]] += 1

        ws = []
        for k, v in unique_word.iteritems():
            ws.append((k.decode('utf8'), (v *1.0)/len(ts)))
        return ws

    @classmethod
    def BuildIndexForOne(cls, db, qId, question):
        logger.debug("build index for one %d %s" % (qId, question))
        ws = cls.GetWords(question)
        for w in ws:
            item = DBItem(w[0], qId, w[1])
            (k, v) = item.Encode()
            db.Put(k, v)



if __name__ == "__main__":
    os.chdir(workPath)
    if len(sys.argv) != 2:
        print "Usage: %s cfg" % sys.argv[0]
        sys.exit()

    if not CheckSingle(single):
        logger.error("another question build instance is running")
        sys.exit()

    dbPath = GetConfigValue("DB_PATH", sys.argv[1])
    if dbPath[-1] == '/':
        dbPath = dbPath[:-1]
    if CheckFileExist(dbPath + ".tmp"):
        DeleteFolders(dbPath + ".tmp")
    index = Index(dbPath + ".tmp")
    index.CreateDB()
    dialogs = BaseDialog.objects.all()
    for d in dialogs:
        try:
            index.BuildIndexForOne(index.db, d.pk, d.question)
        except:
            logger.error(traceback.format_exc())

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

    os.rename(dbPath+".tmp", dbPath)
    searchScript = GetConfigValue("SEARCH_SCRIPT", sys.argv[1])
    print searchScript
    if searchScript != None:
        subprocess.Popen("%s %s" % (searchScript, sys.argv[1]), shell=True)
    RemoveSingle(single)
        
