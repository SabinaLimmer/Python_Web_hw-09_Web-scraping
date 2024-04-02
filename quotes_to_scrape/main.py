from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from quotes_to_scrape.spiders.quotes_spider import QuotesSpider

def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.start()

if __name__ == "__main__":
    main()