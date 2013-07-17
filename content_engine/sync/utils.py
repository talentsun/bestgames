#encoding=utf-8
import time
import os
import re
from content_engine import settings

#FIXME
MAKING_IMAGES_PATH = '/data/media/bestgames/making_images/'

def make_image(content_id, content):
    folder_path = MAKING_IMAGES_PATH + time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if os.path.exists(folder_path):
       pass
    else:
      os.makedirs(folder_path)

    current_time = time.strftime('%H-%M-%S',time.localtime(time.time()))
    file_name = '%s_%d.html' % (current_time, content_id)
    html_file = open(folder_path + '/' + file_name,'w')
    html_file.write(content)
    html_file.close()

    output_file_path = folder_path + "/" + str(content_id) + ".png"
    command = '%s/sync/phantomjs --disk-cache=yes --max-disk-cache-size=10000 %s/sync/rasterize.js %s %s' % (settings.PROJECT_ROOT, settings.PROJECT_ROOT, folder_path + '/' + file_name, output_file_path)
    os.system(command)

    return output_file_path

def convert_youku_video_url(origin_url):
    match = re.search('id_(\w+)\.html', origin_url)
    if match is not None:
        return 'http://player.youku.com/embed/%s' % match.group(1)
    else:
        return origin_url
