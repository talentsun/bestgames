#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from portal.models import Game, Redier, Collection, Problem, Entity, Weixin, Player, News
from breve import Template, flatten
from breve.tags.html import tags
from utils import make_image
import os

TEMPLATE_ROOT = os.path.split(os.path.realpath(__file__))[0] + '/templates/'
t = Template(tags, root=TEMPLATE_ROOT)

class WeiboMessage(object):
    def __init__(self, message, image, entity_id):
        self.message = message
        self.image = image
        self.entity_id = entity_id

def _shorten_text(origin_text, shorten_len=140):
    if len(origin_text) > shorten_len:
        return '%s... ' % origin_text[:110]
    else:
        return origin_text

def build_game_message(game):
    content = t.render('game', dict(
        template_path = TEMPLATE_ROOT,
        screenshot_path_1 = game.screenshot_path_1.path,
        screenshot_path_2 = game.screenshot_path_2.path,
        screenshot_path_3 = game.screenshot_path_3.path,
        screenshot_path_4 = game.screenshot_path_4.path
        ))
    if game.video_url != '':
        weibo_status = _shorten_text(game.recommended_reason, 113) + game.video_url
    else:
        weibo_status = _shorten_text(game.recommended_reason, 133)
    return WeiboMessage(u'#游戏推荐# ' + weibo_status, make_image(game.id, content), game.id)

def build_redier_message(redier):
    content = t.render('redier', dict(
        template_path = TEMPLATE_ROOT,
        redier_image = redier.image_url.path
        ))
    if redier.video_url != '':
        weibo_status = _shorten_text(redier.recommended_reason, 112) + redier.video_url
    else:
        weibo_status = _shorten_text(redier.recommended_reason, 132)
    return WeiboMessage(u'#小兵变大咖# ' + weibo_status, make_image(redier.id, content), redier.id)

def build_collection_message(collection):
    games = []
    for game in collection.games.all():
        games.append({
            'game_img' : game.screenshot_path_1.path,
            'game_name' : game.name,
            'game_icon' : game.icon.path,
            'game_rating' : game.rating,
            'game_size' : '123MB', #FIXME
            'game_category' : game.category.name,
            'game_brief_comment' : game.brief_comment
            })
    content = t.render('collection', dict(
        template_path = TEMPLATE_ROOT,
        games = games,
        collection_cover = collection.cover.path,
        collection_title = collection.title
        ))
    return WeiboMessage(u'#游戏合集# ' + _shorten_text(collection.recommended_reason, 133), make_image(collection.id, content), collection.id)

def build_problem_message(problem):
    content = t.render('problem', dict(
        template_path = TEMPLATE_ROOT,
        problem_image = problem.image_url.path
        ))
    if problem.video_url != '':
        weibo_status = _shorten_text(problem.recommended_reason, 111) + problem.video_url
    else:
        weibo_status = _shorten_text(problem.recommended_reason, 131)
    return WeiboMessage(u'#宅，必有一技# ' + weibo_status, make_image(problem.id, content), problem.id)

def build_player_message(player):
    if player.video_url != '':
        weibo_status = _shorten_text(player.recommended_reason, 120) + player.video_url
    else:
        weibo_status = _shorten_text(player.recommended_reason)
    return WeiboMessage(weibo_status, player.image_url.path, player.id)

def build_news_message(news):
    if news.video_url != '':
        weibo_status = _shorten_text(news.recommended_reason, 112) + news.video_url
    else:
        weibo_status = _shorten_text(news.recommended_reason, 132)
    return WeiboMessage(u'#游戏情报站# ' + weibo_status, news.image_url.path, news.id)