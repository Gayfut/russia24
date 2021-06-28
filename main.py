"""main file for start scraper and show his work"""
from scraper.scraper import Scraper


if __name__ == "__main__":
    scraper = Scraper()
    # all scraped info about posts from Russia24 site
    info = scraper.start_scraping()
    # save info in json file
    scraper.dump_in_json(info)
    # output info in console
    print(info)
