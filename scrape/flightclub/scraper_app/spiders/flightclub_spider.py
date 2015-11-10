#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website flightclub.com and
save to a database (postgres).

Scrapy spider part - it actually performs scraping.
"""
import scrapy

from scrapy.spider import BaseSpider
from scrapy import Selector

from scraper_app.items import FlightClubDeal

import logging

logger = logging.getLogger('example')
logging.basicConfig(filename="flightclub.log", level=logging.DEBUG)


class LivingSocialSpider(BaseSpider):
    """
    Spider for regularly updated flightclub.com site, air jordan page
    """
    name = "fcny"
    allowed_domains = ["flightclub.com"]


    def start_requests(self):
        yield scrapy.Request( "http://www.flightclub.com/air-jordans?id=34&p=1", callback=self.first_parse)
 
    def first_parse(self, response):
        page_count = int(response.xpath('//div[@class="page-counter"]/text()').re("(\d+)\s*$")[0])
        for i in range(2, page_count+1):
            yield scrapy.Request( "http://www.flightclub.com/air-jordans?id=34&p={0}".format(i), callback=self.next_parse)
        for product in response.xpath('//a[contains(@class, "product-image")]/@href').extract():
            yield scrapy.Request(product, callback=self.parse_items)

    def next_parse(self, response):
        for product in response.xpath('//a[contains(@class, "product-image")]/@href').extract():
            yield scrapy.Request(product, callback=self.parse_items)
            
            

    def parse_items(self, response):
        sel = Selector(response)
        item = FlightClubDeal()
        item["title"] = sel.xpath("//title/text()").extract()[0]
        item["link"] = response.url
        item["image"] = sel.xpath("//img[contains(@src,'thumbnail')]/@src").extract()
        if len(item["image"]) < 1:
            item["image"] = sel.xpath("//img[contains(@src,'product')]/@src").extract()
        style = response.xpath('//ul/li[@class="attribute-list-item"][1]/text()').extract()[1]
        styles = style.split()
        #if len(styles) > 2:
        if len(styles[0]) < 7:
            item["style"] = styles[0]
            item["colorcode"] = styles[1]
        else:
            item["nikesku"] = styles[0]
        yield item
