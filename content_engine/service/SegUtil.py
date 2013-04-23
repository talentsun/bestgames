#!/usr/local/bin/python2.7
#coding:utf8


import PySeg
import os, os.path

class SegUtil:
    @classmethod
    def Init(cls, path):
        PySeg.init(path)
        customWordPath = os.path.join(path, "custom_word")
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

    @classmethod
    def SegForLtp(cls, content):
        words = PySeg.seg(content)
        res = []
        for w in words:
            res.append((w[0].decode('utf8').encode('gb2312'), cls.ConvertPosICT2Ltp(w[1])))
        return tuple(res)

    @classmethod
    def ConvertPosICT2Ltp(cls, pos):
        converts = [('nr', 'nh'), ('ns', 'ns'), ('nt', 'ni'), ('n', 'n'), ('t', 'nt'), ('s', 'nl'), ('f', 'nd'), ('v', 'v'), ('an', 'b'), ('a', 'a'), ('b', 'a'), ('z', 'a'), ('r', 'r'), ('m', 'm'), ('q', 'q'), ('d', 'd'), ('p', 'p'), ('c', 'c'), ('u', 'u'), ('e', 'e'), ('y', 'u'), ('o', 'o'), ('h', 'h'), ('k', 'k'), ('x', 'x'), ('w', 'wp')]
        for t in converts:
            if pos[0:len(t[0])] == t[0]:
                return t[1]
        return 'x'


if __name__ == '__main__':
    SegUtil.Init("..")
    words = "有什么好游戏推荐吗？"
    parts = SegUtil.Seg(words)
    for p in parts:
        print p[0].decode("utf8"), p[1]
    parts = SegUtil.SegForLtp(words)
    for p in parts:
        print p[0].decode("gb2312"), p[1]


