import os
import json
def tokenize(document,language):
    if language == 'fr':
        from spacy.lang.fr import French
        nlp = French()
        sentencizer = nlp.create_pipe("sentencizer")
        nlp.add_pipe(sentencizer)
        doc = nlp(document)
        sentences = [[str(word) for word in sent if str(word) != '\n'] for sent in doc.sents]
        return sentences
    else:
        return []

class TextProcessor:
    def __init__(self, text_folder):
        self.documents = {}
        for filename in os.listdir(text_folder):
            with open(text_folder + filename, encoding='utf-8') as file:
                document = json.load(file)
                language = document['language']
                if language in self.documents:
                    self.documents[language].append(document['body'])
                else:
                    self.documents[language] = [document['body']]
    def process(self, normalize=False, punctutation=True):
        self.corpora = {}
        for language,corpus in self.documents.items():
            self.corpora[language] = []
            for document in corpus:
                self.corpora[language].append(tokenize(document,language))