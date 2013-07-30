# -*- coding: utf-8 -*-
from weibo import APIClient
import datetime, time
WEIBO_APP_ID = '1165281516'
WEIBO_APP_SECRET = '4360e65b0e9de717dfe3a0c127bc96b3'
weibo_client = APIClient(WEIBO_APP_ID, WEIBO_APP_SECRET, 'http://cow.bestgames7.com/token/login')
token1='2.00FW7VpD06XASOfcd38a0315rRfGSB'
token2='2.00DfAKsD06XASOeb35f26827y6OR5E'
token3='2.00KfAKsD06XASOb1cfaee579TJcqbD'
token4='2.00JfAKsD06XASO9868c98713q9tliD'
token5='2.00oVVcpD06XASObcda767206danHKB'
token6='2.00pV7VpD06XASO2cbe0a2b89lmoAKB'
token7='2.00AzAKsD06XASO840f531d310WKqIB'
token8='2.00Jj7VpD06XASOd6a86f5232lMWp6C'
token9='2.00ZHu5uD06XASOe5ff59f588eB21bB'
token10='2.00u_6VpD06XASOde84635d98Bx2UFC'
token11='2.00ptasrD06XASO29f00644490YUmk_'
token12='2.00otasrD06XASO125e3334c3HuRkND'
token13='2.00Qpw5uD06XASO92314c18a4DF7esC'
token14='2.00vWUcpD06XASOd1e959638a0AwGnv'
token15='2.004Z6VpD06XASOa09f5fba52NMh8GE'
token16='2.00laUcpD06XASO2cd1618e5arsFsEE'
token17='2.00daUcpD06XASO5faf0a1531tToZQC'
token18='2.002Z6VpD06XASOc01abf8062qQrIKC'
token19='2.00BSbsrD06XASOd4bdeb63d5F6eOVD'
token20='2.00qRbsrD06XASO3bb04859ef_fGxwC'


tokenList=[token1,token2,token3,token4,token5,token6,token7,token8,token9,token10,token11,token12,token13,token14,token15,token16,token17,token18,token19,token20]

hour=datetime.datetime.now().hour
minute=datetime.datetime.now().minute

def  decide_time(hour,minute):
     if (hour==1 and minute==00) or (hour==20 and minute==00):
        return 0
     elif hour==1 and minute ==05 or (hour==20 and minute==05):
        return 1
     elif hour==1 and minute ==10 or (hour==20 and minute==10):
        return 2
     elif hour==1 and minute ==15 or (hour==20 and minute==15):
        return 3
     elif hour==1 and minute ==20 or (hour==20 and minute==20):
        return 4
     elif hour==1 and minute ==25 or (hour==20 and minute==25):
        return 5
     elif hour==1 and minute ==30 or (hour==20 and minute==30):
        return 6
     elif hour==1 and minute ==35 or (hour==20 and minute==35):
        return 7
     elif hour==1 and minute ==40 or (hour==20 and minute==40):
        return 8
     elif hour==1 and minute ==45 or (hour==20 and minute==45):
        return 9
     elif hour==1 and minute ==50 or (hour==20 and minute==50):
        return 10
     elif hour==1 and minute ==55 or (hour==20 and minute==55):
        return 11
     elif hour==2 and minute ==00 or (hour==21 and minute==00):
        return 12
     elif hour==2 and minute ==05 or (hour==21 and minute==05):
        return 13
     elif hour==2 and minute ==10 or (hour==21 and minute==10):
        return 14
     elif hour==2 and minute ==15 or (hour==21 and minute==15):
        return 15
     elif hour==2 and minute ==20 or (hour==21 and minute==20):
        return 16
     elif hour==2 and minute ==25 or (hour==21 and minute==25):
        return 17
     elif hour==2 and minute ==30 or (hour==21 and minute==30):
        return 18
     elif hour==2 and minute ==35 or (hour==21 and minute==35):
        return 19


weibo_client.set_access_token(tokenList[decide_time(hour,minute)],time.time() + 90 * 24 * 3600)


if hour==1 or hour==2:
     weibo_client.post.friendships__create(screen_name=u'每日精品游戏')
if hour==20 or hour==21:
     weibo_client.post.friendships__destory(screen_name=u'每日精品游戏')



 
