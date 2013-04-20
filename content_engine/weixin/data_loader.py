from portal.models import Game, Collection
from django.core.cache import cache
from datetime import date, datetime
from utils import shorten_url
import random

CACHE_TIMEOUT_WEEK = 7 * 24 * 3600


def load_random_games():
    gameIndex = random.randint(0, 20)
    games = Game.objects.all()[gameIndex: gameIndex + 3]
    return games

def load_games_for_today(reload=False):
	if cache.get('games_for_today') and not reload:
		return cache.get('games_for_today')

	year = date.today().year
	month = date.today().month
	day = date.today().day
	start_date = datetime(year, month, day, 0, 0, 0)
	end_date = datetime(year, month, day, 23, 59, 59)

	games = Game.objects.filter(weibo_sync_timestamp__range=(start_date, end_date))
	cache.set('games_for_today', games, (end_date - datetime.today()).total_seconds())
	return games

def _get_game_android_shorten_download_url_key(game):
	return 'g_' + str(game.id) + '_android_d'

def _get_game_ios_shorten_download_url_key(game):
	return 'g_' + str(game.id) + '_ios_d'

def load_shorten_android_download_url(game, reload=False):
	if game.android_download_url is None:
		return None

	android_download_shorten_url = cache.get(_get_game_android_shorten_download_url_key(game))
	if android_download_shorten_url is None or reload:
		android_download_shorten_url = shorten_url(game.android_download_url)
		cache.set(_get_game_android_shorten_download_url_key(game), android_download_shorten_url, CACHE_TIMEOUT_WEEK)
	return android_download_shorten_url

def load_shorten_ios_download_url(game, reload=False):
	if game.iOS_download_url is None:
		return None

	ios_download_shorten_url = cache.get(_get_game_ios_shorten_download_url_key(game))
	if ios_download_shorten_url is None or reload:
		ios_download_shorten_url = shorten_url(game.iOS_download_url)
		cache.set(_get_game_ios_shorten_download_url_key(game), ios_download_shorten_url, CACHE_TIMEOUT_WEEK)
	return ios_download_shorten_url

def load_shorten_urls(reload=False):
	for game in Game.objects.all():
		load_shorten_ios_download_url(game, reload)
		load_shorten_android_download_url(game, reload)

def load_latest_game_collection():
	return Collection.objects.latest('id')
