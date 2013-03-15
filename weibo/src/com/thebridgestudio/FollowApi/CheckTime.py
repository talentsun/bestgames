#!/usr/bin/python
#-*- coding: utf-8 -*-

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from weibo import APIClient 
from AppValue import BGApp
from FriendShip import FriendShip

from Operations.models import Operation
from Competitors.models import Competitor
from SendMail import send_mail

import datetime, copy, sys, os, traceback

work_path = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    from Utils import *

    logger = InitLogger("check_time", logging.DEBUG, "log/check_time.log")
    os.chdir(work_path)

