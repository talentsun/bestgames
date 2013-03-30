# -*- coding: utf-8 -*-
import roadmap.Router
from api.models import Game
from message_builder import MessageBuilder

def processor(build_conf):
	return build_conf

router = roadmap.Router(processor)

@router.destination(r'^下载$', pass_obj=False)
def get_download_urls_for_today:
	year = date.today().year
	month = date.today().month
	day = date.today().day
	start_date = datetime.datetime(year, month, day, 0, 0, 0)
	end_date = datetime.datetime(year, month, day, 23, 59, 59)
	return { 'type' : MessageBuilder.TYPE_DOWNLOAD_URL,
		'platform' : MessageBuilder.PLATFORM_WEIXIN,
		'data' : Game.objects.filter(weibo_sync_timestamp__range=(start_date, end_date)) }
