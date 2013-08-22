#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from portal.models import Game, Redier, Collection, Problem, Entity, Weixin, Player, News, Evaluation
from utils import make_image
import os
from django.template.loader import render_to_string

TEMPLATE_ROOT = os.path.split(os.path.realpath(__file__))[0] + '/templates/'

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
    content = str(render_to_string('game_weibo.tpl', {
        'template_path' : TEMPLATE_ROOT,
        'game' : game,
        }))
    entity = Entity.objects.get(id=game.id)
    if entity.status3 == 2:
        message_link = u'【下载】' + 'http://cow.bestgames7.com/d/%s/' % game.id
    else:
        message_link = ''
    if game.video_url is not None and game.video_url != '':
        weibo_status = _shorten_text(game.recommended_reason, 85) + message_link +' '+ u'【视频】' + game.video_url
    else:
        weibo_status = _shorten_text(game.recommended_reason, 110) + message_link
    return WeiboMessage(u'#游戏推荐# ' + weibo_status, make_image(game.id, content), game.id)

def build_puzzle_message(puzzle):
    content = str(render_to_string('puzzle_weibo.tpl', {
        'puzzle_id' : puzzle.id,
        'template_path' : TEMPLATE_ROOT,
        'puzzle_pic' : puzzle.image_url.path,
        'puzzle_content' : puzzle.description,
        'optiona' : puzzle.option1,
        'optionb' : puzzle.option2,
        'optionc' : puzzle.option3,
        'optiond' : puzzle.option4,
    }))

    return WeiboMessage(u'#趣味答题# ' + _shorten_text(puzzle.title, 133), make_image(puzzle.id, content), puzzle.id)
def build_redier_message(redier):
    content = str(render_to_string('redier_weibo.tpl', {
        'template_path' : TEMPLATE_ROOT,
        'image' : redier.image_url.path
        }))
    if redier.video_url is not None and redier.video_url != '':
        weibo_status = _shorten_text(redier.recommended_reason, 112) + redier.video_url
    else:
        weibo_status = _shorten_text(redier.recommended_reason, 132)
    return WeiboMessage(u'#小兵变大咖# ' + weibo_status, make_image(redier.id, content), redier.id)

def build_collection_message(collection):
    games = []
    for game in collection.games.all():
        games.append({
            'screenshot_path_1' : game.screenshot_path_1.path,
            'name' : game.name,
            'icon' : game.icon.path,
            'rating' : game.rating,
            'size' : game.size,
            'category' : game.category.name,
            'brief_comment' : game.brief_comment,
            'recommended_reason' : game.recommended_reason
            })
    content = str(render_to_string('collection_weibo.tpl', {
        'template_path' : TEMPLATE_ROOT,
        'games' : games,
        'cover' : collection.cover.path,
        'title' : collection.title
        }))
    entity = Entity.objects.get(id=collection.id)
    if entity.status3 == 2:
        message_link = u'【下载】' + 'http://cow.bestgames7.com/d/%s/' % collection.id
    else:
        message_link = ''
    return WeiboMessage(u'#游戏合集# ' + _shorten_text(collection.recommended_reason, 110) + message_link, make_image(collection.id, content), collection.id)

def build_problem_message(problem):
    content = str(render_to_string('problem_weibo.tpl', {
        'template_path' : TEMPLATE_ROOT,
        'image' : problem.image_url.path
        }))
    if problem.video_url is not None and problem.video_url != '':
        weibo_status = _shorten_text(problem.recommended_reason, 111) + problem.video_url
    else:
        weibo_status = _shorten_text(problem.recommended_reason, 131)
    return WeiboMessage(u'#宅，必有一技# ' + weibo_status, make_image(problem.id, content), problem.id)

def build_player_message(player):
    if player.video_url is not None and player.video_url != '':
        weibo_status = _shorten_text(player.recommended_reason, 120) + player.video_url
    else:
        weibo_status = _shorten_text(player.recommended_reason)
    return WeiboMessage(weibo_status, player.image_url.path, player.id)

def build_news_message(news):
    content_items = {'template_path' : TEMPLATE_ROOT}
    if news.screenshot_path_1:
        content_items['screenshot_path_1'] = news.screenshot_path_1.path
    if news.screenshot_path_2:
        content_items['screenshot_path_2'] = news.screenshot_path_2.path
    if news.screenshot_path_3:
        content_items['screenshot_path_3'] = news.screenshot_path_3.path
    if news.screenshot_path_4:
        content_items['screenshot_path_4'] = news.screenshot_path_4.path
    content = str(render_to_string('news_weibo.tpl', content_items))
    if news.video_url is not None and news.video_url != '':
        weibo_status = _shorten_text(news.recommended_reason, 112) + news.video_url
    else:
        weibo_status = _shorten_text(news.recommended_reason, 132)
    return WeiboMessage(u'#游戏情报站# ' + weibo_status, make_image(news.id, content), news.id)



def build_evaluation_message(evaluation):
    content = str(render_to_string('evaluation_weibo.tpl', {
        'template_path': TEMPLATE_ROOT,
        'title': evaluation.title,
        'icon': evaluation.icon.path,
        'rating': evaluation.rating,
        'comment': evaluation.brief_comment,
        'content': evaluation.content,
        'android': evaluation.android_download_url,
        'ios': evaluation.iOS_download_url,
        }))
    entity = Entity.objects.get(id=evaluation.id)   
    if entity.status3 == 2:
        message_link = u'【详情】' + 'http://cow.bestgames7.com/d/%s/' % evaluation.id
    else:
        message_link = ''  
    weibo_status = _shorten_text(evaluation.recommended_reason, 110) + message_link

    return WeiboMessage(u'#游戏测评# '+weibo_status, make_image(evaluation.id, content), evaluation.id)
