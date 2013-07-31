#encoding=utf-8
import time
import datetime
import cronjobs

from sync.weibo import APIClient
from portal.models import Entity
from analyse.models import WeiboCount

WEIBO_APP_ID = '1165281516'
WEIBO_APP_SECRET = '4360e65b0e9de717dfe3a0c127bc96b3'
weibo_client = APIClient(WEIBO_APP_ID, WEIBO_APP_SECRET, 'http://cow.bestgames7.com/token/login')
weibo_client.set_access_token('2.00_WfRrC06XASOb0e30929c0ZKmYeC',time.time() + 90 * 24 * 3600)


@cronjobs.register
def update_weibo_count():
    weibos = WeiboCount.objects.all()
        for weibo in weibos:
            if (datetime.datetime.now()-weibo.sync_timestamp1).days < 7: 
                weibo_get = weibo_client.get.statuses__count(ids=weibo.entity.message_id1)[0]
                comments = weibo_get['comments']
                reposts = weibo_get['reposts']
                weibo.comments = comments
                weibo.reposts = reposts
                weibo.save()
