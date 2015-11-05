#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website flightclub.com and
save to a database (postgres).

Scrapy spider part - it actually performs scraping.
"""
import scrapy

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scraper_app.items import FlightClubDeal


class LivingSocialSpider(BaseSpider):
    """
    Spider for regularly updated flightclub.com site, air jordan page
    """
    name = "fcny"
    allowed_domains = ["flightclub.com"]
    start_urls = ["http://www.flightclub.com/air-jordans/air-jordan-1"]

    def parse(self, response):
        next_page_url = response.xpath('//*[@id="entire-page-wrap"]//div[@class="pages"]/a[@title="Next"]/@href').extract()[0]
        yield scrapy.Request(next_page_url)
        for product in response.xpath('//a[contains(@class, "product-image")]/@href').extract():
            print product
            yield scrapy.Request(product, callback=self.parse_items)

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = FlightClubDeal()
        item["title"] = hxs.select("//title/text()").extract()[0]
        item["link"] = response.url
        item["image"] = hxs.select("//img[contains(@src,'thumbnail')]/@src").extract()
        style = hxs.select('//li/text()').re(r'\d{6}')
        if style:
            item["style"] = style[0]
            item["colorcode"] = hxs.select('//li/text()').re(r'\s(\d{3})')[0]
        print item
        yield item
