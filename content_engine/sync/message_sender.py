#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from weibo import APIClient
from weixin import WeixinClient
from portal.models import Entity
from analyse.models import Weibo_count
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import logging
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

WEIBO_APP_ID = '1165281516'
WEIBO_APP_SECRET = '4360e65b0e9de717dfe3a0c127bc96b3'
weibo_client = APIClient(WEIBO_APP_ID, WEIBO_APP_SECRET, 'http://cow.bestgames7.com/token/login')
weibo_client.set_access_token('2.00baJBTD06XASO9cd01cb598m7o2_B', '1363460399')

weixin_client = WeixinClient()

web_client = Client("http://www.bestgames7.com/xmlrpc.php", 'bestgames', 'nameLR9969')

logger = logging.getLogger("sync")

class MessageSender(object):
	@classmethod
	def send_weibo(self, weibo_message):
		try:
			post_id=weibo_client.statuses.upload.post(status=weibo_message.message, pic=open(weibo_message.image))['id']
			result = 2
		except Exception, e:
			result = 3

		logger.info('send weibo result: %s' % result)
		#Entity.objects.filter(id=weibo_message.entity_id).update(status1=result)
		entity = Entity.objects.get(pk=weibo_message.entity_id)
		entity.status1 = result
		entity.message_id1 = post_id
		entity.save()
		Weibo_count.objects.create(entity_id=weibo_message.entity_id,comments=0,reposts=0,sync_timestamp1=entity.sync_timestamp1)

	@classmethod
	def send_weixin(self, weixin_message):
		result = 3
		if weixin_client.send(weixin_message):
			result = 2

		logger.info('send weixin result: %s' % result)
		Entity.objects.filter(id=weixin_message.entity_id).update(status2=result)

	@classmethod
	def send_web(self, web_message):
		post_id = web_client.call(NewPost(web_message.post))
		result = 3
		if post_id != -1:
			result = 2

		logger.info('send web result: %s' % result)
		Entity.objects.filter(id=web_message.entity_id).update(status3=result, message_id3=post_id)

