#!usr/bin/env bash

# be sure to change both virtualenv directory and scrape/flightclub
# directory to where your venv and code is.
source $WORKON_HOME/scrape/bin/activate
cd ~/Projects/new-coder/scrape/flightclub/scraper_app
scrapy crawl fcny
