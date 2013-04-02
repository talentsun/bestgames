#!/usr/local/bin/python2.7
#coding:utf8


import PySeg
import os, os.path

class SegUtil:
    @classmethod
    def Init(cls, path):
        PySeg.init(path)
        customWordPath = os.path.join(path, "CustomWord")
        if not os.path.exists(customWordPath):
            return 
        for fileName in os.listdir(customWordPath):
            path = os.path.join(customWordPath, fileName)
            wordFile = file(path)
            while True:
                line = wordFile.readline()
                if len(line) == 0:
                    break
                PySeg.addUserWord(line.decode("utf8").encode("gbk"))
            wordFile.close()

    @classmethod
    def Seg(cls, content):
        return PySeg.seg(content)


if __name__ == '__main__':
    SegUtil.Init("..")
    parts = SegUtil.Seg("苹果电脑")
    for p in parts:
        print p[0].decode("utf8")


