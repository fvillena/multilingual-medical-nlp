# -*- coding: utf-8 -*-
import scrapy
import re
import html
import random
class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['egms.de']
    start_urls = ['https://www.egms.de/static/en/journals/index.htm']

    custom_settings={ 'FEED_URI': "journals.csv",
                       'FEED_FORMAT': 'csv'}
    def parse(self, response):
        journals = []
        for link in response.xpath('//a/@href').extract():
            m = re.search(r'journals\/(\w+)\/', link)
            if m:
                journals.append(m.group(1))
        journals = list(set(journals))
        for journal in journals:
            journal_url = "https://www.egms.de/static/en/journals/"+journal+"/archive.htm"
            req = scrapy.Request(journal_url, callback=self.parse_journal)
            yield req
    def parse_journal(self, response):
        for volume in response.xpath('//a/@href').extract():
            if bool(re.search(r"volume\d+\.htm", volume)):
                print(volume)
                req = scrapy.Request("https://www.egms.de" + volume, callback=self.parse_volume)
                yield req
    def parse_volume(self, response):
        for article in response.xpath('//a/@href').extract():
            if bool(re.search(r"static\/(en|de)\/journals\/.*htm", article)):
                req = scrapy.Request("https://www.egms.de" + article, callback=self.get_article_xml)
                yield req
    def get_article_xml(self, response):
         for xml in response.xpath('//a/@href').extract():
             if bool(re.search(r"static\/xml", xml)):
                 req = scrapy.Request("https://www.egms.de" + xml, callback=self.download_xml)
                 yield req
    def download_xml(self, response):
        print("downloading :"+response.url)
        identifier = response.xpath("//GmsArticle//MetaData//Identifier/text()").extract_first()
        filename = '../../data/raw/ges/%s.xml' % identifier
        with open(filename, 'wb') as f:
            f.write(response.body)
