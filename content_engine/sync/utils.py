#encoding=utf-8
from __future__ import division
import time
import os
import re
from content_engine import settings
from PIL import Image
import images2gif

#FIXME
MAKING_IMAGES_PATH = '/data/media/bestgames/making_images/'
MAKING_GIFS_PATH = '/data/media/bestgames/making_gif/'

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

def make_gif(content):
    src_images = []
    images = []

    max_height = 1
    max_width = 1

    folder_path = MAKING_GIFS_PATH + time.strftime('%Y-%m-%d', time.localtime(time.time()))
    target_path = folder_path + "/" + str(content.id) + ".gif"
    if os.path.exists(folder_path):
       pass
    else:
      os.makedirs(folder_path)
    src_icon = None
    if content.type == 1:
        if content.icon.name:
            src_icon = content.icon.path

    if content.screenshot_path_1.name:
        src_images.append(content.screenshot_path_1.path)
    if content.screenshot_path_2.name:
        src_images.append(content.screenshot_path_2.path)
    if content.screenshot_path_3.name:
        src_images.append(content.screenshot_path_3.path)
    if content.screenshot_path_4.name:
        src_images.append(content.screenshot_path_4.path)

    if len(src_images) == 1:
        return src_images[0]

    for image in src_images:
        image_file = open(image, 'rb')
        width, height = Image.open(image_file).size
        max_width = max(width, max_width)
        max_height = max(height, max_height)

    scale = max_height / max_width

    if src_icon:
        image_file = open(src_icon, 'rb')
        img = Image.open(image_file)
        if max_width > max_height:
            icon_resize = img.resize((int(scale * 400), int(scale * 400)), Image.ANTIALIAS)
            background = Image.new("RGB", [400, int(400 * scale)], (255, 255, 255))
            background.paste(icon_resize, ((400 - int(400 * scale))//2, 0))
        elif max_width < max_height:
            icon_resize = img.resize((int(400 / scale), int(400 / scale)), Image.ANTIALIAS)
            background = Image.new("RGB", [int(400 / scale), 400], (255, 255, 255))
            background.paste(icon_resize, (0, (400 - int(400 / scale))//2))
        images.append(background)
        image_file.close()

    for image in src_images:

        image_file = open(image, 'rb')
        img = Image.open(image_file)
        if max_width > max_height:
            img_resize = img.resize((400, int(400 * scale)), Image.ANTIALIAS)
            background = Image.new("RGB", [400, int(400 * scale)], (255, 255, 255))
        elif max_width < max_height:
            img_resize = img.resize((int(400 / scale), 400), Image.ANTIALIAS)
            background = Image.new("RGB", [int(400 / scale), 400], (255, 255, 255))
        background.paste(img_resize, (0, 0))
        images.append(background)
        image_file.close()

    images2gif.writeGif(target_path, images, duration=2, nq=0.1)

    return target_path

