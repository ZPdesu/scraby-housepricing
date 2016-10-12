from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from housepricing.items import HouseDataItem


class AnjukeSpider(CrawlSpider):
    name = 'anjuke'
    allow_domains = ['http://beijing.anjuke.com/']
    start_urls = ['http://beijing.anjuke.com/sale']
    rules = [Rule(sle(allow=r'/p\d+/#filtersort'), follow=True, callback='parse')]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        for site in sites:
            item = HouseDataItem()
            item['url'] = site.xpath('div[@class="house-details"]/div[@class="house-title"]/a/@href').extract()
            item['area'] = site.xpath('div[@class="house-details"]/div[@class="details-item"]/span[1].text()').extract()
            item['room_shape'] = site.xpath('div[@class="house-details"]/div[@class="details-item"]/span[2].text()').extract()
            item['average_price'] = site.xpath('div[@class="house-details"]/div[@class="details-item"]/span[3].text()').extract()
            item['floor'] = site.xpath('div[@class="house-details"]/div[@class="details-item"]/span[4].text()').extract()
            item['floor'] = site.xpath('div[@class="house-details"]/div[@class="details-item"]/span[5].text()').extract()
            item['location'] = site.xpath('div[@class="house-details"]/div[@class="details-item"]/span[@class="comm-address"].text()').extract()
            item['price'] = site.xpath('div[@class="house-details"]/div[@class="pro-price"]/span/strong.text()').extract()
            yield item
