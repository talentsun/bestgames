__author__ = 'huwei'
from scrapy.contrib.loader import XPathItemLoader
import sys
from scrapy.spider import BaseSpider
from auto_get_pic.NetUtils import NetUtil
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
import os

class parsePic(BaseSpider):
    name="parse_ituns"
    reload(sys)
    downloadNet = NetUtil()
    sys.setdefaultencoding('utf-8')
    iconTag =''
    pic_prefix=''


    allowed_domains = ["itunes.apple.com"]

    def __init__(self):
        pass

    def __init__(self,url=None,pic_prefix=None):
        self.start_urls = [url]
        index = url.find('?')
        if index == -1:
            index = len(url)
        print 'index = ' + str(index)
        self.pic_prefix = pic_prefix
        iconTag = url[0:index - 1]
        print iconTag

    def parse(self, response):
        print '1'
        hxs = HtmlXPathSelector(response)

        #TODO use current project path
        root_path = os.getcwd() + "/games/"

        if os.path.exists(root_path):
            pass
        else:
            os.makedirs(root_path)

        print root_path

        iconUrl = hxs.select('//a[contains(@href, iconTag)]/div[@class="artwork"]/img/@src').extract()
        descUrl = hxs.select('//div[@class="lockup"]/img/@src').extract()
        print descUrl
        for icon in iconUrl:
            if icon.find('175x175-75.jpg') != -1:
                print icon
                print root_path
                print self.pic_prefix
                self.downloadNet.download(icon,root_path + 'icon' + self.pic_prefix + ".jpg");
                break;

        count = 1
        for url in descUrl:
            if count <=4:
                self.downloadNet.download(url, root_path + 'desc' + str(count) + self.pic_prefix + ".jpg")
                count = count + 1
            else:
                break;

