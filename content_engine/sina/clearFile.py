import os
import MySQLdb as mdb
import datetime
import time


def getUselessFile():
    con = mdb.connect('localhost', 'root',
        'nameLR9969', 'content_engine',charset='utf8');

    cur = con.cursor()

    curtime = datetime.datetime.fromtimestamp(time.time()-7*24*3600).strftime('%Y-%m-%d')

    print 'start: ' + curtime
    sql = "SELECT  games.icon,games.screenshot_path_1,games.screenshot_path_2,games.screenshot_path_3,games.screenshot_path_4,entities.weibo_sync_timestamp from entities,games where entities.weibo_sync_timestamp  like '" + curtime + "%'  and games.entity_ptr_id = entities.id and entities.status = '2'"
    cur.execute(sql)
    data = cur.fetchall()
    rootPath = '/home/app_bestgames/content_engine/media/';
    for result in data:
        e =  os.path.exists(rootPath + result[0])
        if e:
            os.remove(rootPath + result[0])
        e =  os.path.exists(rootPath + result[1])
        if e:
            os.remove(rootPath + result[1])
        e =  os.path.exists(rootPath + result[2])
        if e:
            os.remove(rootPath + result[2])
        e =  os.path.exists(rootPath + result[3])
        if e:
            os.remove(rootPath + result[3])
        e =  os.path.exists(rootPath + result[4])
        if e:
            os.remove(rootPath + result[4])


    sql = "SELECT collections.cover,entities.weibo_sync_timestamp from entities,collections where entities.weibo_sync_timestamp  like '" + curtime + "%'  and collections.entity_ptr_id = entities.id and entities.status = '2'"
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        e =  os.path.exists(rootPath + result[0])
        if e:
            os.remove(rootPath + result[0])

    sql = "SELECT rediers.redier_image,entities.weibo_sync_timestamp from entities,rediers where entities.weibo_sync_timestamp  like '" + curtime + "%'  and rediers.entity_ptr_id = entities.id and entities.status = '2'"
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        e =  os.path.exists(rootPath + result[0])
        if e:
            os.remove(rootPath + result[0])

    sql = "SELECT problems.problem_image,entities.weibo_sync_timestamp from entities,problems where entities.weibo_sync_timestamp  like '" + curtime + "%'  and problems.entity_ptr_id = entities.id and entities.status = '2'"
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        e =  os.path.exists(rootPath + result[0])
        if e:
            os.remove(rootPath + result[0])


    e = os.path.exists(rootPath + curtime)
    if e:
        os.rmdir(rootPath + curtime)

    if con:
        con.close()

getUselessFile()