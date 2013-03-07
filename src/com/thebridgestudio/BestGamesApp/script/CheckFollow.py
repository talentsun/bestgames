#!/usr/bin/python
# -*- coding: UTF-8 -*-

from weibo import APIClient
from AppValue import BGApp

from SendMail import send_mail

from Operation import Operation
from FriendShip import FriendShip

import time, sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
    else:
        num = 0
    ops = Operation.FetchSomeDayOps(Operation.FollowType, num)
    print "all number %d" % len(ops)
    followNum = 0
    client = APIClient(BGApp.wdj_app_key, BGApp.wdj_app_secret)
    client.set_access_token(BGApp.wdj_me_token, time.time() + 90 * 24 *3600)
    for op in ops:
        try:
            if FriendShip.CheckFollow(client, op.uid, BGApp.dev_uid):
                print op.uid, op.ts
                followNum += 1
            else:
                print "not follow:", op.uid, op.ts
        except:
            pass
        time.sleep(1)
    print "follow num %d" % followNum
    content = "昨天收听了%d个人，%d个人回粉" % (len(ops), followNum)
    send_mail(['bestgames@thebridgestudio.net',], "增粉日报", content)
