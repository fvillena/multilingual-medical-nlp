import json
import hashlib
import os
class ScieloParser:
    def __init__(
        self,
        txt_files_folder
    ):
        self.files = []
        for file in os.listdir(txt_files_folder):
            self.files.append(txt_files_folder + file)
    def parse(self, destination_folder):
        for file in self.files:
            with open(file, encoding="utf-8") as article:
                document = article.read()
                lines = document.split('\n')
                language = 'es'
                title = lines[1]
                body = "\n".join(lines[2:])
            document = {
                'language' : language,
                'title' : title,
                'body' : body
            }
            with open(destination_folder + hashlib.md5(file.encode('utf-8')).hexdigest() + language +".json","w", encoding='utf-8') as jsonfile:
                json.dump(document,jsonfile,ensure_ascii=False, indent=2)