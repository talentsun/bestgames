#!/usr/local/bin/python2.7

import sys
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

import socket, struct

from portal.models import Game

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!HI", 2, Game.objects.all()[0].pk), ("127.0.0.1", 8128))



