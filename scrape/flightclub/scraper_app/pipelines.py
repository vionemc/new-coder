#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website flightclub.com and
save to a database (postgres).

Scrapy pipeline part - stores scraped items in the database.
"""

from sqlalchemy.orm import sessionmaker
from models import Deals, Images, db_connect, create_deals_table


class FlightClubPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """Initializes database connection and sessionmaker.

        Creates deals table.

        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
#        if len(item['image']) > 1:
#            for i in range(len(item['image'])):
#                item['image'][i] = item['image'][i][:50] + item['image'][i][item['image'][i].find('/a/i'):]
#            imagestr = ','.join(item['image'])
#            item['image'] = imagestr
#        else:
#            item['image'] = ""

        session = self.Session()
        deal_item = item.copy()
        del deal_item['image']
        deal = Deals(**deal_item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        for i in item['image']:
            image = Images(link=item['link'], image=i)
            try:
                session.add(image)
                session.commit()
            except:
                session.rollback()
                raise

        return item
