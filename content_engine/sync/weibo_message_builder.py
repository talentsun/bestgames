#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from portal.models import Game, Redier, Collection, Problem, Entity, Weixin, Player, GameAdvices
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

def build_game_message(game):
    content = t.render('game', dict(
        template_path = TEMPLATE_ROOT,
        screenshot_path_1 = game.screenshot_path_1.path,
        screenshot_path_2 = game.screenshot_path_2.path,
        screenshot_path_3 = game.screenshot_path_3.path,
        screenshot_path_4 = game.screenshot_path_4.path
        ))
    return WeiboMessage(u'#游戏推荐# ' + game.recommended_reason, make_image(game.id, content), game.id)

def build_redier_message(redier):
    content = t.render('redier', dict(
        template_path = TEMPLATE_ROOT,
        redier_image = redier.redier_image.path
        ))
    return WeiboMessage(u'#小兵变大咖# ' + redier.recommended_reason, make_image(redier.id, content), redier.id)

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
    return WeiboMessage(u'#游戏合集# ' + collection.recommended_reason, make_image(collection.id, content), collection.id)

def build_problem_message(problem):
    content = t.render('problem', dict(
        template_path = TEMPLATE_ROOT,
        problem_image = problem.problem_image.path
        ))
    return WeiboMessage(u'#宅，必有一技# ' + problem.recommended_reason, make_image(problem.id, content), problem.id)

def build_player_message(player):
    return WeiboMessage(u'#我是玩家# ' + player.recommended_reason, player.player_image.path, player.id)

def build_news_message(news):
    return WeiboMessage(u'#游戏情报站# ' + news.recommended_reason, news.advice_image.path, news.id)