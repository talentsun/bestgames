#!/usr/local/bin/python2.7

import sys, time, os, logging
workPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(workPath + "/..")
import socket, subprocess

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

from portal.models import Game
logger = logging.getLogger("default")


from weixin.data_loader import load_shorten_urls


if __name__ == '__main__':
    load_shorten_urls()



