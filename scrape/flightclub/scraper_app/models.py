#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website flightclub.com and
save to a database (postgres).

Database models part - defines table for storing scraped data.
Direct run will create the table.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.

    Returns sqlalchemy engine instance.

    """
    return create_engine(URL(**settings.DATABASE))


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Deals(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "deals"

    title = Column('title', String(255))
    link = Column('link', String(255), primary_key=True)
    style = Column('style', String(6), nullable=True)
    colorcode = Column('colorcode', String(3), nullable=True)
    nikesku = Column('nikesku', String(255), nullable=True)

class Images(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "images"

    link = Column('link', String(255), ForeignKey('deals.link'))
    image = Column('image', String(255), primary_key=True)
