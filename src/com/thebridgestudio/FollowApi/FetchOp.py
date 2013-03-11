#!/usr/bin/python

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from weibo import APIClient 
from AppValue import BGApp

import datetime, copy, sys, os
from FriendShip import FriendShip

work_path = os.path.dirname(os.path.abspath(__file__))
singleFilePath = "competitor.single"


from Competitors.models import Competitor
from Operations.models import Operation


if __name__ == '__main__':
    from Utils import *
    os.chdir(work_path)

    logger = InitLogger("follow_competitor", logging.DEBUG, "log/follow_competitor.log")
    try:
        if not CheckSingle(singleFilePath):
            sys.exit("another instance running")
        comsDb = Competitor.objects.filter(isTarget=1)
        logger.debug("competitor len %d" % len(comsDb))
        comsWeb = copy.deepcopy(comsDb)
        client = APIClient(BGApp.app_key, BGApp.app_secret)
        client.set_access_token(BGApp.other_token, time.time() + 90 * 24 *3600)
        Competitor.GetNumbers(client, comsWeb)
        ops = Operation.GetSomeDayOps(datetime.date.today())
        for comDb in comsDb:
            for comWeb in comsWeb:
                if comDb.uid == comWeb.uid:
                    logger.debug("web followers %d db followers %d" % (comWeb.followers, comDb.followers))
                    if comWeb.followers > comDb.followers:
                        num = comWeb.followers - comDb.followers
                        logger.debug("%d's followers increase %d" % (comWeb.uid, num))
                        if num > 1:
                            num = 1
                        followers = comWeb.GetFollowers(client, num)
                        for user in followers:
                            op = Operation()
                            op.opUid = user['id']
                            if not FriendShip.CheckFollow(client, BGApp.dev_uid, op.opUid) and len(ops) < 100:
                                FriendShip.Follow(client, op.opUid)
                                op.state = 1
                            else:
                                op.state = 0
                            op.srcUid = comDb.uid
                            logger.debug("new to follow %d" % op.opUid)
                            op.state = 1
                            op.followers = user['followers_count']
                            op.friends = user['friends_count']
                            op.statuses = user['statuses_count']
                            op.save()

        RemoveSingle(singleFilePath)
    except Exception as e:
        RemoveSingle(singleFilePath)
        traceback.print_exc()
        logger.debug(traceback.format_exc())

