#!/usr/local/bin/python2.7
#coding: utf8

import sys
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

import socket, struct

from portal.models import Game
from SearchIndex import SearchIndex

if __name__ == '__main__':
    index = SearchIndex("../testdb", "..")

    index.InitSeg()
    print index.Search(u"3D")




