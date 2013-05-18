#!/usr/local/bin/python2.7
#coding:utf-8
import time,random, sys, logging
sys.path.append('..')

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

lastRewardTime = time.time()
reloadRewardInternal = 3600*24 #每天5次
reloadRewardNums = [5, 20]

rewardNums = [5, 20]
maxDrawTime = 100
rewardResources = {1:{}, 2:{}}
rewardLeftNums = []

logFileName = "../logs/reward.log"
logFile = None

logger = logging.getLogger('default')

userDrawTimes = {}

from draw_pb2 import *

def InitResource():
    reward2 = ['TDD91UVEXV3KG50EXQ',
    'TDD91VZ4MNG68GU997',
    'TDD91YSHEMQV3X8B78',
    'TDD91YZCXSKPRSWJSE',
    'TDD925WV36R3MPJUO4',
    'TDD928JO33B2KV40MH',
    'TDD92EQQCHO6S68FQV',
    'TDD92Q2HHA2B19P4XZ',
    'TDD92VAZ5Y13KUVYOU',
    'TDD932CFV042X8Q12U',
    'TDD9335C91ZIAM3GJS',
    'TDD93CD36YMBCHZM6P',
    'TDD93HEK9FGIBARRF2',
    'TDD93HHD6MENVPFTQF',
    'TDD93R97K404PC6F15',
    'TDD944TOGMT4QXNNJS',
    'TDD946JSAHK9Z38JNZ',
    'TDD94B17CIXXOYOBX5',
    'TDD94VLIRNXHA7367P',
    'TDD950XEX9J2GZ58UU',
    'TDD954E99XOYH5U6SC',
    'TDD959CU2CFKCR8XUL',
    'TDD95N819EDBJ27FYC',
    'TDD96IKF8121SSX00R',
    'TDD96ULG2XVS3PV2WB',
    'TDD96Y7B0QBUYY9D5S',
    'TDD96Z9UYCR2OW1VSC',
    'TDD972H4H12X4OB2HH',
    'TDD973NO8T01382MI8',
    'TDD975OC3ILELFMUA5',
    'TDD97I8GT809N97O2S',
    'TDD97VG8E8XY2Z7L89',
    'TDD97Z310K5ZWA1C69',
    'TDD989ZBL9G6L29X0V',
    'TDD98FIB1R6DZCXKGZ',
    'TDD98TY3EOSPQJDHMR',
    'TDD98UT1DU3FWIWX0W',
    'TDD99MFYMYA4F7WYTJ',
    'TDD99U4P6QD4KI520P',
    'TDD99X4VH4HMDJVNZO',
    'TDD9AO3A1O7NP3E6LS',
    'TDD9AYJHWMMQT2B15I',
    'TDD9B11RMB0ETXVNT6',
    'TDD9B5LAYXHZAOG5VS',
    'TDD9B8X4WZVREX18AO',
    'TDD9BAKW6MZ4L2116Y',
    'TDD9BTAACLAOJ8D6BI',
    'TDD9BTLLX4FOEL2LMU',
    'TDD9BWBA0CVN4SIKYC',
    'TDD9BXB64EJF19TDPR',
    'TDD9C3DR2WDGVZFXLP',
    'TDD9COHANCQA9VBJ8W',
    'TDD9CQRIV8X47CF68V',
    'TDD9D41XJR4FDSTP9Q',
    'TDD9D5TVPMPNIU3HRQ',
    'TDD9DI03DKXQNYZ27G',
    'TDD9DJBNO0IRSLIZLT',
    'TDD9DKLX57JMQWLABD',
    'TDD9DLU2VQN80GV0S2',
    'TDD9DOZL3NFB0BC3WB']

    reward1 = ['TDDO6SMVK3DZU87DLG',
    'TDDO6TPQXO0KGB3N8P',
    'TDDO6WOY1RS8P3JV4T',
    'TDDO75ZM0SDNIIZO36',
    'TDDO7766GQYWJ8EB9Z',
    'TDDO7O6G6CXE3V4OSA',
    'TDDO7OUIUU94873SFP',
    'TDDO7Z4CZFMWY0JN72',
    'TDDO8GQN7B31Y9RG0T',
    'TDDO8JUK9OCKUZEU9E',
    'TDDO91559DLBK2JJXM',
    'TDDO94BRR6ARUAXJ6N',
    'TDDO9B19D0946OJ2BN',
    'TDDO9HMWXQMX30SPO4',
    'TDDO9NUANPUR5D9TOD']

    for i in reward1:
        rewardResources[1][i] = 1
    for i in reward2:
        rewardResources[2][i] = 1
    pass
def InitReward():
    global logFile
    num = 0
    rewardLeftNums.append(0)
    for i in range(len(rewardNums)):
        rewardLeftNums.append(rewardNums[i])
        num += rewardNums[i]
    noRewardNum = 0
    if maxDrawTime > num:
        noRewardNum = maxDrawTime - num
    rewardLeftNums[0] = noRewardNum
    
    RedoLog()
    logFile = file(logFileName, 'a+')
def RedoLog():
    global lastRewardTime, userDrawTimes
    readLogFile = file(logFileName, "r")
    while True:
        line = readLogFile.readline().strip()
        if len(line) < 1:
            break
        seps = line.split()
        type = int(seps[0])
        if type == 1:
            rid = int(seps[1])
            uid = seps[2]
            if uid not in userDrawTimes:
                userDrawTimes[uid] = 0
            userDrawTimes[uid] += 1
            if len(seps) == 4:
                res = seps[3]
            else:
                res = ""
            if rewardLeftNums[rid] > 0:
                rewardLeftNums[rid] -= 1
            if rid in rewardResources and res in rewardResources[rid] and rewardResources[rid][res] > 0:
                rewardResources[rid][res] -= 1
        elif type == 2:
            ReloadReward(True)
            lastRewardTime = int(seps[1])
    readLogFile.close()
def ReloadReward(redo = False):
    userDrawTimes = []
    global logFile, lastRewardTime, reloadRewardInternal
    num = 0
    for i in range(len(reloadRewardNums)):
        rewardLeftNums[i+1] += reloadRewardNums[i]
        num += rewardLeftNums[i+1]
    noRewardNum = 0
    if maxDrawTime > num:
        noRewardNum = maxDrawTime - num
    rewardLeftNums[0] = noRewardNum
    if not redo:
        lastRewardTime += reloadRewardInternal
        logFile.write("2 %d\n" % int(lastRewardTime))
        logFile.flush()
    
def GetResource(reward):
    if reward not in rewardResources:
        return ""
    res = rewardResources[reward]
    for k,v in res.items():
        if v>0:
            res[k] -= 1
            return k
    return ""

def Draw(uid):
    global userDrawTimes
    if uid in userDrawTimes and userDrawTimes[uid] >= 3:
        return (-1, "", 0)
    if uid not in userDrawTimes:
        userDrawTimes[uid] = 0
    userDrawTimes[uid] += 1
    global logFile, lastRewardTime, reloadRewardInternal
    now = time.time()
    if now > lastRewardTime + reloadRewardInternal:
        ReloadReward()
    base = 0
    for i in range(len(rewardLeftNums)):
        base += rewardLeftNums[i]
    if base == 0:
        return (0, GetResource(0), 3 - userDrawTimes[uid])
    item = random.randrange(base)
    for i in range(len(rewardLeftNums)):
        if item < rewardLeftNums[i]:
            rewardLeftNums[i] -= 1
            res = GetResource(i)
            logFile.write("1 %d %s %s\n" % (i, uid, res))
            logFile.flush()
            return (i, res, 3 - userDrawTimes[uid])
        else:
            item -= rewardLeftNums[i]
    print "error"
    return (0, GetResource(0), 3 - userDrawTimes[uid])
def StartServer(port):
    import socket
    host = "127.0.0.1"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    while True:
        try:
            message, address = s.recvfrom(8192)
            logger.debug("len %d" % len(message))
            query = DrawQuery()
            query.ParseFromString(message)
            resp = DrawResp()
            resp.result = 0
            resp.reward, resp.value, resp.leftTimes = Draw(query.uid)
            print resp.reward, resp.value, resp.leftTimes
            s.sendto(resp.SerializeToString(), address)
        except KeyboardInterrupt:
            break
        except:
            logger.error(traceback.format_exc())


     

if __name__ == '__main__':
    InitResource()
    InitReward()
    StartServer(8040)
