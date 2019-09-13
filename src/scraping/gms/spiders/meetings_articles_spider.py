# -*- coding: utf-8 -*-
import scrapy
import re
import html
import random
class MeetingArticlesSpider(scrapy.Spider):
    name = 'meeting_articles'
    allowed_domains = ['egms.de']
    start_urls = ['https://www.egms.de/static/en/meetings/index.htm']

    custom_settings={ 'FEED_URI': "meetings.csv",
                       'FEED_FORMAT': 'csv'}
    def parse(self, response):
        journals = []
        for link in response.xpath('//a/@href').extract():
            m = re.search(r'meetings\/(\w+)\/', link)
            if m:
                journals.append(m.group(1))
        journals = list(set(journals))
        for journal in journals:
            journal_url = "https://www.egms.de/dynamic/en/meetings/"+journal+"/index.htm"
            req = scrapy.Request(journal_url, callback=self.parse_journal)
            yield req
    def parse_journal(self, response):
        for volume in response.xpath('//a/@href').extract():
            if bool(re.search(r"main=", volume)):
                print(volume)
                req = scrapy.Request("https://www.egms.de" + volume, callback=self.parse_volume)
                yield req
    def parse_volume(self, response):
        for article in response.xpath('//a/@href').extract():
            if bool(re.search(r"static\/(en|de)\/meetings\/.*htm", article)):
                req = scrapy.Request("https://www.egms.de" + article, callback=self.get_article_xml)
                yield req
    def get_article_xml(self, response):
         for xml in response.xpath('//a/@href').extract():
             if bool(re.search(r"static\/xml", xml)):
                 req = scrapy.Request("https://www.egms.de" + xml, callback=self.download_xml)
                 yield req
    def download_xml(self, response):
        # print("downloading :"+response.url)
        identifier = response.xpath("//GmsArticle//MetaData//Identifier/text()").extract_first()
        filename = '../../data/raw/gms/%s.xml' % identifier
        with open(filename, 'wb') as f:
            f.write(response.body)
