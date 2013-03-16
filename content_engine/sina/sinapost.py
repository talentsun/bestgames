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

def sendWeibo(weibostatus,pic,game_id):
    client.statuses.upload.post(status=weibostatus ,
                                  pic=open(pic))
    con = mdb.connect('localhost', 'root',
        'nameLR9969', 'content_engine');

    cur = con.cursor()
    sql = "update entities set status = '2' where id = '" + str(game_id) + "';"
    print sql
    cur.execute(sql)
    con.commit()
    con.close()

def imageBuilder(pic1,pic2,pic3,pic4,game_id,weibo_status):
    templete_file = open('./templete/game.html','r')
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
    templete_file = open('./templete/redier.html','r')
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

def redier():
    con = mdb.connect('localhost', 'root',
        'nameLR9969', 'content_engine',charset='utf8');

    cur = con.cursor()
    curtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    print 'start: ' + curtime
    #curtime = '2013-03-15 10:31:00'
    sql = "SELECT rediers.entity_ptr_id,rediers.redier_image,entities.weibo_sync_timestamp, entities.recommended_reason from entities,rediers where entities.weibo_sync_timestamp  like '" + curtime + "%'  and rediers.entity_ptr_id = entities.id "
    print sql
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        redierImageBuidler(result[0],result[1],result[3])

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
    sql = "SELECT games.name, games.entity_ptr_id,games.screenshot_path_1,games.screenshot_path_2,games.screenshot_path_3,games.screenshot_path_4,entities.weibo_sync_timestamp, entities.recommended_reason from entities,games where entities.weibo_sync_timestamp  like '" + curtime + "%'  and games.entity_ptr_id = entities.id "
    print sql
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        print result[7]
        imageBuilder(result[2],result[3],result[4],result[5],result[1],result[7].decode('utf-8'))

    redier()
finally:
    if con:
        con.close()
