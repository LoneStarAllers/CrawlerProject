# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:46:41 2020

@author: Parham
"""

# Beautiful Soup

import requests
from bs4 import BeautifulSoup
from csv import writer

response = requests.get("http://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")
quotes = soup.find_all("div", class_="quote")

with open("quotes_data.csv", 'w') as csv_file:
    
    csv_writer = writer(csv_file)
    csv_writer.writerow(["Text", "Author", "Tags"])

    for quote in quotes:
        text = quote.find("span").get_text()
        author = quote.find("small").get_text()
        a_tags = quote.find("div", class_="tags").find_all("a")
        tags = []
        for a_tag in a_tags:
            tags.append(a_tag.get_text())
        csv_writer.writerow([text, author, tags])
        


# Scrapy

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }

