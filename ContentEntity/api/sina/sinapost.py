from api.sina.weibo import  APIClient
import MySQLdb as mdb
import time
import datetime
import threading

_APP_ID = '1483181040'    
_APP_SECRET = '6f503ed72723bacf9f4a0f4902b62c24'

client = APIClient(_APP_ID, _APP_SECRET, 'http://account.wandoujia.com/v1/user/?do=platform_sina')
client.set_access_token('2.00wsGZQCqIR4cB8ac1f7170aj5evFC', '7809909')

def sendWeibo(weibostatus,pic):
    client.statuses.upload.post(status=weibostatus ,
                                  pic=open(pic))

con = None

try:
    # con = mdb.connect('localhost', 'root',
    #     'nameLR9969', 'content_entity');

    con = mdb.connect('localhost', 'root',
        '20120811', 'bestgames');

    cur = con.cursor()

    curtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    sql = "SELECT hot_games.name, Entities.timestamp,recommended_reason from Entities,hot_games where timestamp  between \'" +  curtime + " 00:00:00\' and \'" + curtime + " 23:59:59\'  and hot_games.entity_id_id = Entities.id"
    #print sql
    cur.execute(sql)
    data = cur.fetchall()
    for result in data:
        name = result[0]
        print str(result[1])
        timestamp = time.mktime(datetime.datetime.strptime(str(result[1]), "%Y-%m-%d %H:%M:%S").timetuple())
        reason = result[2]
         # timestamp - time.time()
        t = threading.Timer(timestamp - time.time(),sendWeibo,(reason,'/Users/huwei/test.png'))
        t.start()
finally:
    if con:
        con.close()
