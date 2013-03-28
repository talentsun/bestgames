from scrapy.contrib.loader import XPathItemLoader
import sys
from parseApple.items import ParseappleItem
from scrapy.spider import BaseSpider
from parseApple.NetUtil import NetUtil
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector


class parseIcon(BaseSpider):
    name="parseituns"
    reload(sys)
    downloadNet = NetUtil()
    sys.setdefaultencoding('utf-8')
    url =''

    allowed_domains = ["itunes.apple.com"]
    start_urls = [
        "https://itunes.apple.com/cn/app/ninja-fishing/id445283501?mt=8"
    ]

    def __init__(self,url):
        self.url = url

    def parse(self, response):
        print '1'
        hxs = HtmlXPathSelector(response)

        iconUrl = hxs.select('//a[contains(@href, "https://itunes.apple.com/cn/app/ninja-fishing/id445283501")]/div[@class="artwork"]/img/@src').extract()
        print iconUrl
        self.downloadNet.download(iconUrl[0],'image1' + ".jpg");
