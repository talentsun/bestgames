import sys,os,time

mysql_usr='root'
mysql_pwd='nameLR9969'
mysql_db='content_engine'
mysql_charset='gb2312'

today=time.strftime('%Y-%m-%d')
fname=today+'-'+time.strftime('%H%M%S')+'.gz'

cmd_dump = 'mysqldump -u%s -p%s %s | gzip > %s' % (mysql_usr, mysql_pwd, mysql_db, fname)

def writeLogs(filename,contents):
  f = file(filename,'aw')
  f.write(contents)
  f.close()

logs_path = os.getcwd() + "/logs"
if os.system(cmd_dump)==0:
  writeLogs(logs_path + '/back_up_log', 'database backup: ' + fname + '\n')
  os.system('mv %s %s' % (fname, logs_path))
else:
  writeLogs(logs_path + '/back_up_log', 'database backup failed! \n')
