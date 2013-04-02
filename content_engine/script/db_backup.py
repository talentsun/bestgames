import sys,os,time

mysql_usr='root'
mysql_pwd='nameLR9969'
mysql_db='content_engine'
mysql_charset='gb2312'

today=time.strftime('%Y-%m-%d')
fname=today+'-'+time.strftime('%H%M%S')+'.gz'

cmd_dump = 'mysqldump -u%s -p%s %s | gzip > %s' % (mysql_usr, mysql_pwd, mysql_db, fname)

if os.system(cmd_dump)==0:
  writeLogs(logs_path, 'database backup: ' + fname + 'n')
else:
  writeLogs(logs_path, 'database backup failed! n')
