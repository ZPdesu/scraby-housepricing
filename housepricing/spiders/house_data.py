from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from housepricing.items import HouseDataItem


class AnjukeSpider(CrawlSpider):
    name = 'anjuke'
    allow_domains = ['http://beijing.anjuke.com/']
    start_urls = ['http://beijing.anjuke.com/sale']
    rules = [Rule(sle(allow='/p\d+/#filtersort'), follow=True, callback='parse_site')]

    def parse_site(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul[@id="houselist-mod"]/li')

        for site in sites:

            item = HouseDataItem()
            item['url'] = site.xpath('div[@class="house-details"]/div[1]/a/@href').extract()
            item['area'] = site.xpath('div[@class="house-details"]/div[2]/span[1]/text()').extract()
            item['room_shape'] = site.xpath('div[@class="house-details"]/div[2]/span[2]/text()').extract()
            item['average_price'] = site.xpath('div[@class="house-details"]/div[2]/span[3]/text()').extract()
            item['floor'] = site.xpath('div[@class="house-details"]/div[2]/span[4]/text()').extract()
            item['build_time'] = site.xpath('div[@class="house-details"]/div[2]/span[5]/text()').extract()
            item['location'] = site.xpath('div[@class="house-details"]//span[@class="comm-address"]/text()').extract()
            item['price'] = site.xpath('div[@class="pro-price"]/span/strong/text()').extract()
            yield item

