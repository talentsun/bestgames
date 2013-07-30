#encoding=utf-8
from sync.weibo import APIClient
import time
import datetime
from portal.models import Entity
from analyse.models import Weibo_count
import cronjobs

WEIBO_APP_ID = '1165281516'
WEIBO_APP_SECRET = '4360e65b0e9de717dfe3a0c127bc96b3'
weibo_client = APIClient(WEIBO_APP_ID, WEIBO_APP_SECRET, 'http://cow.bestgames7.com/token/login')
weibo_client.set_access_token('2.00_WfRrC06XASOb0e30929c0ZKmYeC',time.time() + 90 * 24 * 3600)


@cronjobs.register
def update_weibo_count():
        weibos=Weibo_count.objects.all()
 	for weibo in weibos:
            entity=Entity.objects.get(pk = weibo.entity_id)
            if (datetime.datetime.now()-entity.sync_timestamp1).days<=7: 
               message_id=entity.message_id1
               myweibo= weibo_client.get.statuses__count(ids=message_id)[0]
               comments=myweibo['comments']
               reposts=myweibo['reposts']
               weibo_in_database=Weibo_count.objects.get(entity_id=weibo.entity_id)
               weibo_in_database.comments=comments
               weibo_in_database.reposts=reposts
               weibo_in_database.sync_timestamp1=entity.sync_timestamp1
               weibo_in_database.save()
