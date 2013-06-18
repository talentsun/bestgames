#usr/bin/env python
#! -*- coding:utf-8 -*-
import os, subprocess
app_names = [
            'django_tables2','django-datetime-widget', 'django-select2', \
            'pycURL', 'django-cronjobs','python-wordpress-xmlrpc', \
            'python-memcached', 'django-memcached','django-social-auth', \
            'django-dajax'
            ]

failed_apps = []

cmd1 = 'sudo apt-get install python-setuptools'
cmd2 = 'sudo easy_install pip'
cmd3 = 'sudo pip install'
cmd4 = 'sudo python setup.py install'

#install pip
def install_tool():
    for cmd in [cmd1, cmd2]:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        if p.returncode != 0:
            failed_apps.append(cmd.split(' ')[1:])
    print '##########Tools Installation Finished!##########'

#install apps from PyPI
def install_app():
    for app_name in app_names:
        p =  subprocess.Popen(cmd3+' '+app_name, stdout=subprocess.PIPE, shell=True)
        p.wait()
        if p.returncode == 0:
            print'#%s installed successfully'% app_name
        else:
            failed_apps.append(app_name)

#install apps of /bestgames/content_engine/libs
def install_libs():
    path = '../libs/'
    names = os.listdir(path)
    #find all folders
    all_dir_names = [x for x in names if os.path.isdir(path+x)]

    #find all folders which within setup.py
    dirnames=[]
    for dirname in all_dir_names:
        filenames = os.listdir(path+dirname)
        for filename in filenames:
            if filename == 'setup.py':
                dirnames.append(dirname)

    #shell commands
    for dirname in dirnames:
        p = subprocess.Popen(cmd4, stdout=subprocess.PIPE, cwd=path+dirname, shell=True)
        p.wait()
        if p.returncode == 0:
            print '#%s installed successfully'% dirname
        else:
             failed_apps.append(dirname)

if __name__ == '__main__':
    install_tool()
    install_app()
    install_libs()
    print '##########Installation Finished!##########'
    for name in failed_apps:
        print '#%s is failed to install'% name
