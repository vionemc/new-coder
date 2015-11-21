#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website flightclub.com and
save to a database (postgres).

Scrapy spider part - it actually performs scraping.
"""
import scrapy
import cfscrape

from scrapy.spider import BaseSpider
from scrapy import Selector

from scraper_app.items import FlightClubDeal

import logging

logger = logging.getLogger('example')
logging.basicConfig(filename="endclothing.log", level=logging.DEBUG)


class EndClothingSpider(BaseSpider):
    """
    Spider for regularly updated endclothing.com site, air jordan page
    """
    name = "endclothing"
    allowed_domains = ["endclothing.com"]
    token, agent = cfscrape.get_tokens("http://www.endclothing.com/us/latest-products/latest-sneakers")


    def start_requests(self):
        yield scrapy.Request( "http://www.endclothing.com/us/latest-products/latest-sneakers",
                      cookies=self.token,
                      headers={'User-Agent': self.agent},callback=self.first_parse)
 
    def first_parse(self, response):
        next_url = response.xpath('//div[@class="pager"]//a[@title="Next"]/@href').extract()[0]
        print next_url
        yield scrapy.Request( next_url,
                  cookies=self.token,
                  headers={'User-Agent': self.agent}, callback=self.next_parse)
        for product in response.xpath('//a[contains(@class, "product-image")]/@href').extract():
            token, agent = cfscrape.get_tokens(product)
            yield scrapy.Request(product,
                  cookies=token,
                  headers={'User-Agent': agent},
                  callback=self.parse_items)

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
        try:
            style = response.xpath('//ul/li[@class="attribute-list-item"][1]/text()').extract()[1]
            styles = style.split()
            #if len(styles) > 2:
            if len(styles[0]) < 7:
                item["style"] = styles[0]
                item["colorcode"] = styles[1]
            else:
                item["nikesku"] = styles[0]
        except IndexError: pass
        yield item
