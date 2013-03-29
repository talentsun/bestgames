__author__ = 'huwei'
from scrapy.contrib.loader import XPathItemLoader
import sys
from scrapy.spider import BaseSpider
from auto_get_pic.NetUtils import NetUtil
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

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

        iconUrl = hxs.select('//a[contains(@href, iconTag)]/div[@class="artwork"]/img/@src').extract()
        descUrl = hxs.select('//div[@class="lockup"]/img/@src').extract()
        print iconUrl
        for icon in iconUrl:
            if icon.find('175x175-75.jpg') != -1:
                self.downloadNet.download(icon,'icon' + self.pic_prefix + ".jpg");
                break;

        count = 2
        for url in descUrl:
            self.downloadNet.download(url,'image' + str(count) + self.pic_prefix + ".jpg")
            count = count + 1

