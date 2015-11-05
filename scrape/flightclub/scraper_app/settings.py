# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'flightclub'

SPIDER_MODULES = ['scraper_app.spiders']

ITEM_PIPELINES = ['scraper_app.pipelines.FlightClubPipeline']

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',  # fill in your username here
    'password': 'yourpass',  # fill in your password here
    'database': 'scrape'
}
