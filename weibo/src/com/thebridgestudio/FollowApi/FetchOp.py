#!/usr/local/bin/python2.7

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


def GetUserInfo(client, uid):
    pass


if __name__ == '__main__':
    from Utils import *
    os.chdir(work_path)

    logger = InitLogger("follow_competitor", logging.DEBUG, work_path + "/log/follow_competitor.log")
    try:
        if not CheckSingle(singleFilePath):
            sys.exit("another instance running")
        comsDb = Competitor.objects.filter(isTarget=1)
        logger.debug("competitor len %d" % len(comsDb))
        comsWeb = copy.deepcopy(comsDb)
        client = APIClient(BGApp.app_key, BGApp.app_secret)
        client.set_access_token(BGApp.weico_token, time.time() + 90 * 24 *3600)
        Competitor.GetNumbers(client, comsWeb)
        ops = Operation.GetSomeDayOps(datetime.date.today(), 1)
        logger.debug("ops number %d" % len(ops))
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
                            try:
                                op = Operation.objects.get(opUid = user['id'])
                                # already follow once
                                continue
                            except:
                                op = Operation()
                            op.opUid = user['id']
                            op.state = 0
                            if user['followers_count'] < 50:
                                logger.debug("newer")
                                continue

                            if user['friends_count'] > user['followers_count'] * 10:
                                logger.debug("dead user")
                                continue
                            if not FriendShip.CheckFollow(client, BGApp.dev_uid, op.opUid):
                                if comDb.uid == 2171037552: #anzhuoyouxi
                                    if len(ops) < 105:
                                        op.state = 1
                                else:
                                    if len(ops) < 90:
                                        op.state = 1
                            if op.state == 1:
                                logger.debug("follow %d" % op.opUid)
                                FriendShip.Follow(client, op.opUid)
                            else:
                                logger.debug("today has followed %d" % len(ops))
                                continue
                            op.srcUid = comDb.uid
                            op.followers = user['followers_count']
                            op.friends = user['friends_count']
                            op.statuses = user['statuses_count']
                            op.save()

        RemoveSingle(singleFilePath)
    except:
        RemoveSingle(singleFilePath)
        traceback.print_exc()
        logger.debug(traceback.format_exc())

