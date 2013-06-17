#usr/bin/env python
#! -*- coding:utf-8 -*-
import os, subprocess
app_names=['django_tables2','django-datetime-widget', 'django-select2', \
           'pycURL', 'sinaweibopy','django-cronjobs','python-wordpress-xmlrpc', \
           'python-memcached', 'django-memcached','django-social-auth', 'django-dajax']

cmd1 = 'sudo apt-get install python-setuptools'
cmd2 = 'sudo easy_install pip'
cmd3 = 'sudo pip install'

def ToolInstall():
    for cmd in [cmd1, cmd2]:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell = True)
        p.wait()
        if p.returncode != 0:
            print '%s failed'%cmd.split(' ')[1:]
    print '######Tools installation finished!######'

def AppInstall():
    for name in app_names:
        p =  subprocess.Popen(cmd3+' '+name, stdout=subprocess.PIPE, shell = True)
        p.wait()
        if p.returncode == 0:
            print'%s installed successfully'%name
        else:
            print '%s is not installed'%name
    return True

def LibsInstall():
    path = '../libs/'
    names = os.listdir(path)
    #找到所有子文件夹
    AllDirNames = [x for x in names if os.path.isdir(path+x)]
    dirnames=[]
    #找到所有存在setup.py的文件夹
    for dirname in AllDirNames:
        filenames = os.listdir(path+dirname)
        for filename in filenames:
            if filename == 'setup.py':
                dirnames.append(dirname)
    #执行命令
    for dirname in dirnames:
        cmd4 = 'sudo python setup.py install'
        p = subprocess.Popen(cmd4, stdout=subprocess.PIPE, cwd=path+dirname, shell = True)
        p.wait()
        if p.returncode == 0:
            print '%s installed successfully'%dirname
        else:
            print '%s is not installed'%dirname
    return True

if __name__ == '__main__':
    ToolInstall()
    if AppInstall() and LibsInstall():
        print '######Apps installation finished!######'