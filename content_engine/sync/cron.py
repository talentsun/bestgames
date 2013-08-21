#encoding=utf-8
#! usr/local/bin/python
import cronjobs
import datetime
from portal.models import Game, Redier, Collection, Problem, Entity, Weixin, Player, News, Puzzle, Evaluation
from message_sender import MessageSender
import weibo_message_builder
import weixin_message_builder
import web_message_builder
import logging
import sys

sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

logger = logging.getLogger("sync")

@cronjobs.register
def sync():
	logger.info('sync...')
	sync_weibo()
	sync_weixin()
	sync_web()
	logger.info('sync done')

@cronjobs.register
def sync_weibo():
	# query entities needed to sync
	entities = Entity.objects.filter(sync_timestamp1__range=(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(minutes=5)), status1=1)
	for entity in entities:
		weibo_message = None
		if entity.type == Entity.GAME:
			weibo_message = weibo_message_builder.build_game_message(Game.objects.get(id=entity.id))
			logger.info('sync game %s to weibo' % weibo_message.entity_id)
		elif entity.type == Entity.REDIER:
			weibo_message = weibo_message_builder.build_redier_message(Redier.objects.get(id=entity.id))
			logger.info('sync redier %s to weibo' % weibo_message.entity_id)
		elif entity.type == Entity.COLLECTION:
			weibo_message = weibo_message_builder.build_collection_message(Collection.objects.get(id=entity.id))
			logger.info('sync collection %s to weibo' % weibo_message.entity_id)
		elif entity.type == Entity.PROBLEM:
			weibo_message = weibo_message_builder.build_problem_message(Problem.objects.get(id=entity.id))
			logger.info('sync problem %s to weibo' % weibo_message.entity_id)
		elif entity.type == Entity.PLAYER:
			weibo_message = weibo_message_builder.build_player_message(Player.objects.get(id=entity.id))
			logger.info('sync player %s to weibo' % weibo_message.entity_id)
		elif entity.type == Entity.PUZZLE:
			weibo_message = weibo_message_builder.build_puzzle_message(Puzzle.objects.get(id=entity.id))
			logger.info('sync puzzle %s to weibo' % weibo_message.entity_id)
		elif entity.type == Entity.NEWS:
			weibo_message = weibo_message_builder.build_news_message(News.objects.get(id=entity.id))
			logger.info('sync news %s to weibo' % weibo_message.entity_id)
		elif entity.type == Entity.EVALUATION:
			weibo_message = weibo_message_builder.build_evaluation_message(Evaluation.objects.get(id=entity.id))
			logger.info('sync evaluation %s to weibo' % weibo_message.entity_id)
		if weibo_message is not None:
			MessageSender.send_weibo(weibo_message)
		else:
			logger.info('nothing to sync to weibo')

@cronjobs.register
def sync_weixin():
	#query weixin messages
	weixin_msgs = Weixin.objects.filter(sync_timestamp2__range=(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(minutes=5)), status2=1)
	for msg in weixin_msgs:
		logger.info('sync msg %s to weixin' % msg.id)
		MessageSender.send_weixin(weixin_message_builder.build_weixin_message(msg))

@cronjobs.register
def sync_web():
	#query entities needed to sync
	entities = Entity.objects.filter(sync_timestamp3__range=(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(minutes=5)), status3=1)
	for entity in entities:
		web_message = None
		if entity.type == Entity.GAME:
			web_message = web_message_builder.build_game_message(Game.objects.get(id=entity.id))
			logger.info('sync game %s to web' % entity.id)
		if entity.type == Entity.NEWS:
			web_message = web_message_builder.build_news_message(News.objects.get(id=entity.id))
			logger.info('sync news %s to web' % entity.id)
		if entity.type == Entity.COLLECTION:
			web_message = web_message_builder.build_collection_message(Collection.objects.get(id=entity.id))
			logger.info('sync collection %s to web' % entity.id)
		if entity.type == Entity.PUZZLE:
			web_message = web_message_builder.build_puzzle_message(Puzzle.objects.get(id=entity.id))
			logger.info('sync puzzle %s to web' % entity.id)
		if entity.type == Entity.EVALUATION:
			web_message = web_message_builder.build_evaluation_message(Evaluation.objects.get(id=entity.id))
			logger.info('sync evaluation %s to web' % entity.id)
		if web_message is not None:
			MessageSender.send_web(web_message)
