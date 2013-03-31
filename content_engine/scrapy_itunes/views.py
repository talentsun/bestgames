# Create your views here.
# -*- coding: utf-8 -*-
import sys
import os
from django.http import HttpResponse
import json
import time

def getPic(request):
    root_path = os.path.dirname(os.path.dirname(os.path.normpath(__file__))) + '/scrapy_itunes/auto_get_pic'

    download_url = request.GET.get('download_url')

    curtime = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))

    print download_url
    command = 'cd ' + root_path +  '&&scrapy crawl parse_ituns -a  url=' + download_url + ' -a pic_prefix=' + curtime
    print command
    os.system(command)

    response_data = {}

    server_url = "http://cow.bestgames7.com/tools/url2icon/static/"

    response_data['icon'] = server_url + 'icon' + curtime + ".jpg"
    response_data['desc1'] = server_url + 'desc1' + curtime + ".jpg"
    response_data['desc2'] = server_url + 'desc2' + curtime + ".jpg"
    response_data['desc3'] = server_url + 'desc3' + curtime + ".jpg"
    response_data['desc4'] = server_url + 'desc4' + curtime + ".jpg"

    return HttpResponse(json.dumps(response_data), content_type="application/json")



