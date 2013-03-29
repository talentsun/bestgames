# Create your views here.
# -*- coding: utf-8 -*-
import sys
import os
from django.http import HttpResponse
import json
import time

def getPic(request):
    root_path = '/Users/huwei/games/bestgames/scrapy_itunes/auto_get_pic'

    download_url = request.GET.get('download_url')

    curtime = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))

    print download_url
    command = 'cd ' + root_path +  '&&scrapy crawl parse_ituns -a  url=' + download_url + ' -a pic_prefix=' + curtime
    print command
    os.system(command)

    response_data = {}

    response_data['icon'] = 'icon' + curtime + ".jpg"
    response_data['desc1'] = 'desc1' + curtime + ".jpg"
    response_data['desc2'] = 'desc2' + curtime + ".jpg"
    response_data['desc3'] = 'desc3' + curtime + ".jpg"
    response_data['desc4'] = 'desc4' + curtime + ".jpg"

    return HttpResponse(json.dumps(response_data), content_type="application/json")



