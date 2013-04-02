# coding: utf8
from router import Router
from portal.models import Game
from message_builder import MessageBuilder, BuildConfig
from datetime import date, datetime

def get_download_urls_for_today(rule, info):
	year = date.today().year
	month = date.today().month
	day = date.today().day
	start_date = datetime(year, month, day, 0, 0, 0)
	end_date = datetime(year, month, day, 23, 59, 59)
	return BuildConfig(MessageBuilder.TYPE_DOWNLOAD_URL, None, Game.objects.filter(weibo_sync_timestamp__range=(start_date, end_date)), 'download_urls_for_today', (end_date - datetime.today()).total_seconds())

def get_games_for_today(rule, info):
	year = date.today().year
	month = date.today().month
	day = date.today().day
	start_date = datetime(year, month, day, 0, 0, 0)
	end_date = datetime(year, month, day, 23, 59, 59)
	return BuildConfig(MessageBuilder.TYPE_GAMES, None, Game.objects.filter(weibo_sync_timestamp__range=(start_date, end_date)), 'games_for_today', (end_date - datetime.today()).total_seconds())

Router.get_instance().set({
		'name' : u'获取今日精品推荐游戏的下载地址',
		'pattern' : u'下载',
		'handler' : get_download_urls_for_today
	})
Router.get_instance().set({
		'name' : u'获取今日精品游戏推荐',
		'pattern' : u'(游戏|推荐)',
		'handler' : get_games_for_today
	})
Router.get_instance().set({
		'name' : u'打招呼',
		'pattern' : u'.*(你好|hi|hello|您好).*',
		'handler' : ['你好喽','小每祝您全家发财','好毛啊好']
	})
Router.get_instance().set({
		'name' : u'有病',
		'pattern' : u'.*有病.*',
		'handler' : ['你有药啊！','你妹啊！','春了吧。。。']
	})