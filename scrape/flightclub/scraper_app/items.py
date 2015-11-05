#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website flightclub.com and
save to a database (postgres).

Scrapy item part - defines container for scraped data.
"""

from scrapy.item import Item, Field


class FlightClubDeal(Item):
    """Flightclub container (dictionary-like object) for scraped data"""
    title = Field()
    link = Field()
    image = Field()
    style = Field()
    colorcode = Field()
