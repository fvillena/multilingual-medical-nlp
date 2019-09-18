import os
from bs4 import BeautifulSoup
import json
import hashlib

def normalize_language_name(language):
    if language == 'engl':
        language = 'en'
    if language == 'germ':
        language = 'de'
    if language == 'fren':
        language = 'fr'
    if language == 'ger':
        language = 'de'
    if language == 'eng':
        language = 'en'
    if language == 'deutsch':
        language = 'de'
    if language == 'german':
        language = 'de'
    if language == 'germ225':
        language = 'de'
    if language == 'ebgl':
        language = 'en'
    if language == 'engl.':
        language = 'en'
    return language
def parse_languages(soup):
    languages = [soup.find('language').text]
    if soup.find('languagetranslation'):
        languages.append(soup.find('languagetranslation').text)
    return [normalize_language_name(language) for language in languages]
def parse_title(soup, language):
    try:
        titlegroup = soup.find('titlegroup')
        titles = titlegroup.findChildren(attrs = {'language':language})
        title = titles[0].text
        return title
    except IndexError:
        print('no titles')
def parse_body(soup,language):
    body = []
    blocks = soup.find_all('textblock')
    for block in blocks:
        if ((block.has_attr('language') == False) or (block.get('language') == language)):
            subblocks = []
            for subblock in block.findChildren():
                subblocks.append(subblock.text)
            body.append('\n'.join(subblocks))
    return '\n'.join(body)
class GmsParser:
    def __init__(
        self,
        xml_files_folder
    ):
        self.files = []
        for file in os.listdir(xml_files_folder):
            self.files.append(xml_files_folder + file)
    def parse(self, destination_folder):
        for file in self.files:
            with open(file, encoding="iso-8859-1") as article:
                soup = BeautifulSoup(article.read())
            languages = parse_languages(soup)
            for language in languages:
                title = parse_title(soup,language)
                body=parse_body(soup,language)
                document = {
                    'language' : language,
                    'title' : title,
                    'body' : body
                }
                with open(destination_folder + hashlib.md5(file.encode('utf-8')).hexdigest() + language +".json","w", encoding='utf-8') as jsonfile:
                    json.dump(document,jsonfile,ensure_ascii=False, indent=2)