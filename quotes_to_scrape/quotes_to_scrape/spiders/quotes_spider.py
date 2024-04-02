import scrapy
import unicodedata
from quotes_to_scrape.items import QuoteItem, AuthorItem
import json

def save_json_file(data: list, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self):
        super().__init__()
        self.quotes_list = []
        self.authors_list = []

    def parse(self, response):
        for quote in response.css('div.quote'):
            tags = quote.css('div.tags a.tag::text').getall()
            author_name = quote.css('small.author::text').get().strip()
            quote_text = quote.css('span.text::text').get().strip()
            author_url = response.urljoin(quote.css('span a::attr(href)').get())

            quote_text = unicodedata.normalize('NFKD', quote_text).encode('ascii', 'ignore').decode('utf-8')
            author_name = unicodedata.normalize('NFKD', author_name).encode('ascii', 'ignore').decode('utf-8')

            self.quotes_list.append({
                'tags': tags,
                'author': author_name,
                'quote': quote_text
            })

            yield QuoteItem(
                tags=tags,
                author=author_name,
                quote=quote_text
            )

            yield scrapy.Request(author_url, callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        author_name = response.css('h3.author-title::text').get().strip()
        birth_date = response.css('span.author-born-date::text').get().strip()
        birth_location = response.css('span.author-born-location::text').get().strip()
        description = response.css('div.author-description::text').get().strip()

        author_name = unicodedata.normalize('NFKD', author_name).encode('ascii', 'ignore').decode('utf-8')
        birth_location = unicodedata.normalize('NFKD', birth_location).encode('ascii', 'ignore').decode('utf-8')
        description = unicodedata.normalize('NFKD', description).encode('ascii', 'ignore').decode('utf-8')

        self.authors_list.append({
            'fullname': author_name,
            'born_date': birth_date,
            'born_location': birth_location,
            'description': description
        })

        yield AuthorItem(
            fullname=author_name,
            born_date=birth_date,
            born_location=birth_location,
            description=description
        )

    def closed(self, reason):
        save_json_file(self.quotes_list, 'quotes.json')
        save_json_file(self.authors_list, 'authors.json')
