import os, time, subprocess, shutil, string, re, traceback, signal, logging, logging.handlers
import struct,socket,fcntl

def CheckFileExist(filePath):
    if os.path.exists(filePath):
        return True
    return False
    
def DeleteFile(filePath):
    if CheckFileExist(filePath):
        os.remove(filePath)

def DeleteFolders(filePath):
    if CheckFileExist(filePath):
        shutil.rmtree(filePath)

def GetMd5Value(filePath):
    output = subprocess.Popen(["md5sum " + filePath], stdout=subprocess.PIPE, shell=True).communicate()[0]
    seps = output.split()
    if len(seps) != 2:
        return ""
    return seps[0]
    
def CreateEmptyFile(fileName):
    p = subprocess.Popen(['touch ' + fileName], shell=True)
    p.wait()
    if not CheckFileExist(fileName):
        raise Exception, ['create empty file %s failed' % fileName,]
    pass
    
def CreateEmptyFolder(fileName):
    p = subprocess.Popen(['mkdir ' + fileName], shell=True)
    p.wait()
    if not CheckFileExist(fileName):
        raise Exception, ['create empty folder %s failed' % fileName,]
    pass

def GetPid(processName):
    # 0 is stdout
    output = subprocess.Popen(["ps -o pid= -C " + processName], stdout=subprocess.PIPE, shell=True).communicate()[0]
    pids = output.split()
    if len(pids) < 0:
        return 0
    else:
        return pids[0]
        
def GetPids(processName):
    output = subprocess.Popen(["ps -o pid= -C " + processName], stdout=subprocess.PIPE, shell=True).communicate()[0]
    pids = output.split()
    return pids
    
def CheckSingle(singleFileName):
    if CheckFileExist(singleFileName):
        return False
    CreateEmptyFile(singleFileName)
    return True
    
def RemoveSingle(singleFileName):
    DeleteFile(singleFileName)
    
def GetProcessNum(processName):
    script = "ps -o pid= -C " + processName + " | wc -l"
    output = subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0]
    return int(output)
    
def KillAll(processName):
    script = "killall " + processName
    p = subprocess.Popen([script], shell=True)
    p.wait()
 
def KillOne(pid):
    os.kill(pid, signal.SIGTERM)

def GetPidByNetPort(port):
    script = "lsof -i :%d" % port
    output = subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0]
    lines = output.splitlines()
    if len(lines) <= 1:
        return None
    contentLine = lines[1]
    return int(contentLine.split()[1])

def SendAlarm(userId, msg):
    script = "find /usr/local/tips_agent* -name 'toagent'"
    output = subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0]
    output = string.strip(output)
    print msg
    if len(output) > 0:
        script = output + ' 32 "sms|rtx|mail" "' + userId + '" "' + str(msg) + '" ""'
        p = subprocess.Popen([script], shell=True)
        p.wait()
        
def SendMail(userlist, content):
    script = "find /usr/local/tips_agent* -name 'toagent'"
    output = subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0]
    sendProgram = string.strip(output)
    if len(sendProgram) > 0:
        script = sendProgram + ' 32 "mail" "' + userlist + '" "' + content + '" ""'
        p = subprocess.Popen([script], shell=True)
        p.wait()
        
def PutFile(ip, port, moduleName, remoteFilePath, localFilePath):
    args = ['rsync', '-a', '--bwlimit=10000', localFilePath, 'rsync://' + ip + ':' + str(port) + '/' + moduleName + remoteFilePath]
    p = subprocess.Popen(args)
    p.wait()
    

def FetchFile(ip, port, moduleName, remoteFilePath, localFilePath):
    args = ['rsync', '-a', '--bwlimit=10000', 'rsync://' + ip + ':' + str(port) + '/' + moduleName + remoteFilePath, localFilePath]
    p = subprocess.Popen(args)
    p.wait()
    
def CopyLocalFile(dstFilePath, srvFilePath):
    args = ['rsync', '-a', '--bwlimit=10000', srvFilePath, dstFilePath]
    p = subprocess.Popen(args)
    p.wait()
    
def FindFileInFolderWithPrefix(folderPath, prefixStr):
    fileList = os.listdir(folderPath)
    for fileName in fileList:
        if re.match(prefixStr, fileName):
            return fileName
    return None
    
def RmSharedMem(memId):
    script = "ipcrm -M " + str(memId)
    p = subprocess.Popen(script, shell=True)
    p.wait()
    
def GetConfigValue(configName, configFilePath):
    try:
        configFile = file(configFilePath)
    except:
        print traceback.format_exc()
        return None
    try:
        while True:
            line = configFile.readline()
            if len(line) <= 0:
                break
            parts = line.split()
            if len(parts) >= 2 and parts[0] == configName:
                configFile.close()
                return parts[1]
        configFile.close()
        return None
    except:
        print traceback.format_exc()
        configFile.close()
        return None
        
def DumpPkg(pkg):
    print "dump Pkg len %d" % len(pkg)
    for i in range(len(pkg)):
        seg = ""
        start = ""
        if (i % 16 == 3 or i % 16 == 11):
            seg = " -"
        elif (i % 16 == 7):
            seg = " |"
        elif (i % 16 == 15):
            seg = "\n"
        else:
            seg = ""
        if i % 16 == 0:
            print "%04x: " % i,
        print "%02x%s" % (int(ord(pkg[i])), seg),
    print ""
    
def GetFileLineNum(filePath):
    tmpFile = file(filePath)
    lineNum = 0
    while True:
        line = tmpFile.readline()
        if len(line) == 0:
            break
        lineNum += 1
    tmpFile.close()
    return lineNum
            
def GetEmailListFromIdList(idList):
    ids = idList.split(";")
    emails = ""
    for id in ids:
        if len(id) > 0:
            emails += id + "@tencent.com;"
    return emails[:-1]

def LocalIpAddr(ifname = "eth1"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])
    
def IsMainSrv(cfgFilePath, MAIN_CFG_PATH, BACKUP_CFG_PATH, USE_MAIN_SRV):
    localIp = LocalIpAddr()
    mainCfg = GetConfigValue(MAIN_CFG_PATH, cfgFilePath)
    backupCfg = GetConfigValue(BACKUP_CFG_PATH, cfgFilePath)
    useMain = int(GetConfigValue(USE_MAIN_SRV, cfgFilePath))
    if useMain == 0:
        mainCfg = backupCfg
    srvCfgFile = file(mainCfg, "r")
    while True:
        line = srvCfgFile.readline()
        if len(line) <= 1:
            break
        seps = line.split()
        if seps[0] == localIp:
            srvCfgFile.close()
            return True
    srvCfgFile.close()
    return False
    
    
def InitLogger(loggerName,level,logFileName):
    myLogger = logging.getLogger(loggerName)
    myLogger.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(logFileName, maxBytes=1000000, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))    
    myLogger.addHandler(handler)
    return myLogger
    
def SortFileByColumn(filePath, pos, resultFilePath, tmpFolder="/tmp"):
    script = "sort -k %d -n -T %s %s > %s" % (pos, tmpFolder, filePath, resultFilePath)
    p = subprocess.Popen(script, shell=True)
    p.wait()
    
    
def RecvLen(tcpSock, dataLen):
    data = ""
    while len(data) < dataLen:
        data += tcpSock.recv(dataLen - len(data))
    return data
    
def ChangeConfValue(cfgFileName, cfgName, newValue):
    script = "sed 's/^%s.*$/%s\\t" % (cfgName, cfgName) + str(newValue) + "/' < " + cfgFileName + " > " + cfgFileName + ".tmp"
    p = subprocess.Popen([script], shell=True)
    p.wait()
    os.remove(cfgFileName)
    os.rename(cfgFileName + ".tmp", cfgFileName)
    
def ReloadConfig(procName):
    pids = GetPids(procName)
    for pidStr in pids:
        pid = int(pidStr)
        print "reload config for %d" % pid
        os.kill(pid, signal.SIGUSR1)