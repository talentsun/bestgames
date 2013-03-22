#encoding=utf-8
from weibo import  APIClient
import MySQLdb as mdb
import time
import datetime
import threading
import os
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

_APP_ID = '1165281516'    
_APP_SECRET = '4360e65b0e9de717dfe3a0c127bc96b3'

client = APIClient(_APP_ID, _APP_SECRET, 'http://cow.bestgames7.com/token/login')
client.set_access_token('2.00baJBTD06XASO35dcd07da0NOAOTC', '1363460399')
file_prefix = 'file:///home/app_bestgames/content_engine/sina/';

collection_template='''<td> <div class="game-info">
<img id='game_img' src="%s"></img>
<table>
<tr><td>游戏名称：</td><td>%s</td></tr>
<tr><td>游戏类型：</td><td>%s</td></tr>
<tr><td>游戏评价：</td><td>%s</td></tr>
</table>
<span class="intro">%s</span>
</div>
</td>
'''

def sendWeibo(weibostatus,pic,game_id):
    try:
        client.statuses.upload.post(status=weibostatus ,
                                  pic=open(pic))
        weibo_result = '2'
    except: 
        weibo_result = '3'   
    con = mdb.connect('localhost', 'root',
           'nameLR9969', 'content_engine');

    cur = con.cursor()
    sql = "update entities set status = '"  + str(weibo_result) + "' where id = '" + str(game_id) + "';"
    print sql
    cur.execute(sql)
    con.commit()
    con.close()

def imageBuilder(pic1,pic2,pic3,pic4,game_id,weibo_status):
    templete_file = open('./templates/game.html','r')
    line = templete_file.readline()
    content = ''
    while line:
        content = content + line;
        line = templete_file.readline()

    templete_file.close()


    print pic1 + pic2  
   
    content = content.replace('game_screenshot_1','/home/app_bestgames/content_engine/media/' + pic1)
    content = content.replace('game_screenshot_2','/home/app_bestgames/content_engine/media/' + pic2)
    content = content.replace('game_screenshot_3','/home/app_bestgames/content_engine/media/' + pic3)
    content = content.replace('game_screenshot_4','/home/app_bestgames/content_engine/media/' + pic4)

    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if os.path.exists(today):
       pass
    else:
      os.makedirs(today)

    curtime = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    filename = curtime + 'share.html'
    shareGameFile = open(today + '/' + filename,'w')
    shareGameFile.write(content)
    shareGameFile.close()
    
    outputFilePath = today + "/" + str(game_id) + ".png"

    command = "phantomjs --disk-cache=yes --max-disk-cache-size=10000 rasterize.js "+ file_prefix + today + "/" + filename + "  " + outputFilePath

    print command
    os.system(command)

    sendWeibo('#精品游戏推荐# ' + weibo_status,outputFilePath,game_id)


def redierImageBuidler(game_id,pic,weibo_status):
    templete_file = open('./templates/redier.html','r')
    line = templete_file.readline()
    content = ''
    while line:
        content = content + line;
        line = templete_file.readline()

    templete_file.close()


    content = content.replace('redier_image','/home/app_bestgames/content_engine/media/' + pic)

    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if os.path.exists(today):
       pass
    else:
      os.makedirs(today)

    curtime = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    filename = curtime + 'share.html'
    shareGameFile = open(today + '/' + filename,'w')
    shareGameFile.write(content)
    shareGameFile.close()

    outputFilePath = today + "/" + str(game_id) + "redier.png"

    command = "phantomjs --disk-cache=yes --max-disk-cache-size=10000 rasterize.js "+ file_prefix + today + "/" + filename + "  " + outputFilePath

    print command
    os.system(command)

    sendWeibo('#小兵变大咖# ' + weibo_status,outputFilePath,game_id)

def collectionImageBuilder(gameId,collectionTitle,collectionCover,nameList,screenList,gameBriefList,gameRatingList,gameCategoryList,weibo_status):
    templete_file = open('./templates/collection.html','r')
    line = templete_file.readline()
    content = ''
    while line:
        content = content + line;
        line = templete_file.readline()

    templete_file.close()
    collection_games = ''
    i = 0
    for name in nameList:
        count = gameRatingList[i]
        j = 0
        star = ''
        while j < count :
            star = star + '<div class="star"></div>'
            j = j + 2
        r = count - j

        if r != 0:
            star = star + '<div class="half-star"></div><div class="empty-star"></div>'
        collection_games = collection_games + collection_template%('/home/app_bestgames/content_engine/media/' + screenList[i],name,gameCategoryList[i],star,gameBriefList[i])
        i = i + 1
        if i%2 == 0:
            collection_games = '<tr>%s</tr>' %(collection_games)
        print i

    collection_games = '<tr>%s</tr>' %(collection_games)

    content = content.replace('collection_cover_image','/home/app_bestgames/content_engine/media/' + collectionCover)
    content = content.replace('collection_title',collectionTitle)
    content = content.replace('collection_game',collection_games)

    print content

    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if os.path.exists(today):
        pass
    else:
        os.makedirs(today)

    curtime = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    filename = curtime + 'share.html'
    shareGameFile = open(today + '/' + filename,'w')
    shareGameFile.write(content)
    shareGameFile.close()

    outputFilePath = today + "/" + str(gameId) + "collection.png"

    command = "phantomjs --disk-cache=yes --max-disk-cache-size=10000 rasterize.js "+ file_prefix + today + "/" + filename + "  " + outputFilePath

    print command
    os.system(command)

    sendWeibo('#游戏合集# ' + weibo_status,outputFilePath,gameId)


def problemImageBuidler(game_id,pic,weibo_status):
    templete_file = open('./templates/problem.html','r')
    line = templete_file.readline()
    content = ''
    while line:
        content = content + line;
        line = templete_file.readline()

    templete_file.close()


    content = content.replace('problem_image','/home/app_bestgames/content_engine/media/' + pic)

    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if os.path.exists(today):
        pass
    else:
        os.makedirs(today)

    curtime = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    filename = curtime + 'share.html'
    shareGameFile = open(today + '/' + filename,'w')
    shareGameFile.write(content)
    shareGameFile.close()

    outputFilePath = today + "/" + str(game_id) + "problem.png"

    command = "phantomjs --disk-cache=yes --max-disk-cache-size=10000 rasterize.js "+ file_prefix + today + "/" + filename + "  " + outputFilePath

    print command
    os.system(command)

    sendWeibo('#宅，必有一技# ' + weibo_status,outputFilePath,game_id)


def redier():
    con = mdb.connect('localhost', 'root',
        'nameLR9969', 'content_engine',charset='utf8');

    cur = con.cursor()
    curtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    print 'start: ' + curtime
    #curtime = '2013-03-15 10:31:00'
    sql = "SELECT rediers.entity_ptr_id,rediers.redier_image,entities.weibo_sync_timestamp, entities.recommended_reason from entities,rediers where entities.weibo_sync_timestamp  like '" + curtime + "%'  and rediers.entity_ptr_id = entities.id and entities.status = '1' "
    print sql
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        redierImageBuidler(result[0],result[1],result[3])

    if con:
       con.close()


def collection():
    con = mdb.connect('localhost', 'root',
        'nameLR9969', 'content_engine',charset='utf8');

    cur = con.cursor()
    curtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    print 'start: ' + curtime

    sql = "SELECT collections.entity_ptr_id,collections.title AS collection_title, collections.cover AS collection_cover,games.`name` AS game_name,games.screenshot_path_2 AS game_screenshot,game_entities.brief_comment AS game_brief_comment,game_entities.rating AS game_rating,categories.`name` AS game_category," \
          "collection_entities.weibo_sync_timestamp AS collection_weibo_sync_timestamp,collection_entities.`status` AS collection_status FROM collections INNER JOIN collections_games ON collections.entity_ptr_id = collections_games.collection_id " \
          "INNER JOIN games ON collections_games.game_id = games.entity_ptr_id INNER JOIN entities game_entities ON games.entity_ptr_id = game_entities.id " \
          "INNER JOIN entities collection_entities ON collections.entity_ptr_id = collection_entities.id INNER JOIN categories ON games.category_id = categories.id " \
          "WHERE collection_entities.weibo_sync_timestamp like '"+ curtime +  "%'"
    print sql
    nameList = []
    screenList = []
    gameBriefList = []
    gameRatingList = []
    gameCategoryList = []
    collection_title=''
    collection_cover=''
    gameId = ''
    weibo_status = ''
    cur.execute(sql)

    data = cur.fetchall()

    for result in data:
        gameId = result[0]
        collection_title = result[1]
        collection_cover = result[2]
        nameList.append(result[3])
        screenList.append(result[4])
        gameBriefList.append(result[5])
        gameRatingList.append(result[6])
        gameCategoryList.append(result[7])
        weibo_status = result[8]

    print collection_title
    print collection_cover
    print nameList

    collectionImageBuilder(gameId,collection_title,collection_cover,nameList,screenList,gameBriefList,gameRatingList,gameCategoryList,weibo_status)

    if con:
        con.close()


def problem():
    con = mdb.connect('localhost', 'root',
        'nameLR9969', 'content_engine',charset='utf8');

    cur = con.cursor()
    curtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    print 'start: ' + curtime
    sql = "SELECT problems.entity_ptr_id,problems.problem_image,entities.recommended_reason, entities.weibo_sync_timestamp from entities,problems where entities.weibo_sync_timestamp  like '" + curtime + "%'  and problems.entity_ptr_id = entities.id and entities.status = '1' and entities.type = '4' "
    print sql
    cur.execute(sql)

    data = cur.fetchall()

    for result in data:
        problemImageBuidler(result[0],result[1],result[2])


    if con:
        con.close()



con = None

try:

    con = mdb.connect('localhost', 'root',
        'nameLR9969', 'content_engine',charset='utf8');

    cur = con.cursor()

    curtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    print 'start: ' + curtime
    #curtime = '2013-03-15 10:30:00'
    sql = "SELECT games.name, games.entity_ptr_id,games.screenshot_path_1,games.screenshot_path_2,games.screenshot_path_3,games.screenshot_path_4,entities.weibo_sync_timestamp, entities.recommended_reason from entities,games where entities.weibo_sync_timestamp  like '" + curtime + "%'  and games.entity_ptr_id = entities.id and entities.status = '1'"
    print sql
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        print result[7]
        imageBuilder(result[2],result[3],result[4],result[5],result[1],result[7].decode('utf-8'))

    redier()
    collection()
    problem()

finally:
    if con:
        con.close()
