# coding: utf8
from router import Router
from api.models import Game
from message_builder import MessageBuilder, BuildConfig
from datetime import date
import datetime

def get_download_urls_for_today(rule, info):
	year = date.today().year
	month = date.today().month
	day = date.today().day
	start_date = datetime.datetime(year, month, day, 0, 0, 0)
	end_date = datetime.datetime(year, month, day, 23, 59, 59)
	return BuildConfig(MessageBuilder.TYPE_DOWNLOAD_URL, None, Game.objects.filter(weibo_sync_timestamp__range=(start_date, end_date)))

Router.get_instance().set({
		'name' : u'获取今日推荐游戏的下载地址',
		'pattern' : u'下载',
		'handler' : get_download_urls_for_today
	})