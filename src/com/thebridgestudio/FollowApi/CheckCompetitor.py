#!/usr/bin/python

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from weibo import APIClient 
from AppValue import BGApp

import datetime, copy, sys, os, traceback
from FriendShip import FriendShip

work_path = os.path.dirname(os.path.abspath(__file__))


from Competitors.models import Competitor
from Operations.models import Operation


if __name__ == '__main__':
    from Utils import *
    os.chdir(work_path)

    logger = InitLogger("check_competitor", logging.DEBUG, "log/check_competitor.log")
    try:
        comsDb = Competitor.objects.all()
        logger.debug("competitor len %d" % len(comsDb))
        client = APIClient(BGApp.wdj_app_key, BGApp.wdj_app_secret)
        client.set_access_token(BGApp.wdj_me_token, time.time() + 90 * 24 *3600)
        for com in comsDb:
            com.FetchInfo(client)
            com.save()
            print "name %s" % com.screenName
    except:
        logger.debug(traceback.format_exc())
