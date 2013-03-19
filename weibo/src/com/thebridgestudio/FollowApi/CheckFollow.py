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

    logger = InitLogger("check_follow", logging.DEBUG, "log/check_follow.log")
    os.chdir(work_path)
    unfollowDay = datetime.date.today()
    ops = Operation.GetSomeDayOps(unfollowDay, 1)
    client = APIClient(BGApp.wdj_app_key, BGApp.wdj_app_secret)
    client.set_access_token(BGApp.wdj_me_token, time.time() + 90 * 24 *3600)
    allToFollow = 0
    allFollowers = 0
    followResult = {}
    for op in ops:
        if op.state == 1:
            allToFollow += 1
        else:
            continue
        logger.debug("unfollow %d state %d %s" % (op.opUid, op.state, op.actionTime))
        try:
            if not op.srcUid in followResult:
                followResult[op.srcUid] = [0, 0]
            followResult[op.srcUid][0] += 1
            if FriendShip.CheckFollow(client, op.opUid, BGApp.dev_uid):
                logger.debug("%d follow us" % op.opUid)
                followResult[op.srcUid][1] += 1
                allFollowers += 1
            else:
                logger.debug("%d not follow" % op.opUid)
        except:
            logger.debug(traceback.format_exc())

        time.sleep(1)
    mailContent = ""
    mailContent += "今日一共收听了%d个人，%d个人回粉\n" % (allToFollow, allFollowers)
    mailContent += "其中：\n"
    for (k, v) in followResult.items():
        com = Competitor.objects.get(uid=k)
        mailContent += "%s" % com.screenName.encode('utf_8')
        mailContent += "一共收听了%d个人，回粉了%d个人\n" % (v[0], v[1])

    print mailContent
    send_mail(['bestgames@thebridgestudio.net',], "增粉日报", mailContent)

