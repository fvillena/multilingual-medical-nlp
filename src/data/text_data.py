import os
import json
import hashlib
from spacy.lang.fr import French
from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
def tokenize(document,language,punctutation):
    if language == 'fr':
        nlp = French()
    if language == 'de':
        nlp = German()
    if language == 'en':
        nlp = French()
    if language == 'es':
        nlp = Spanish()
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)
    doc = nlp(document)
    if punctutation:
        sentences = [[str(word) for word in sent if str(word) != '\n'] for sent in doc.sents]
    else:
        sentences = [[str(word) for word in sent if ((str(word) != '\n') and (str(word).isalpha()))] for sent in doc.sents]
    return sentences

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
    def process(self, output_folder, normalize=False, punctutation=True):
        for language,corpus in self.documents.items():
            for document in corpus:
                tokenized_document = tokenize(document,language,punctutation)
                document_to_write = []
                for sentence in tokenized_document:
                    sentence = ' '.join(sentence)
                    document_to_write.append(sentence)
                document_to_write = '\n'.join(document_to_write)
                with open(output_folder + language + '/' + hashlib.md5(document_to_write.encode('utf-8')).hexdigest() +'.txt', 'w') as f:
                    f.write(document_to_write)
class TextAnalyzer:
    def __init__(self, corpora_folder):
        self.files = {language:[] for language in os.listdir(corpora_folder)}
        for language in self.files.keys():
            document_files = [corpora_folder + language + '/' + document_file for document_file in os.listdir(corpora_folder + language)]
            self.files[language] = document_files
    def load_files(self):
        self.corpora = {language:[] for language in self.files.keys()}
        for corpus,files in self.files.items():
            for document_file in files:
                with open(document_file, 'r', encoding='utf-8') as f:
                    article = f.read()
                article = article.replace('\n',' ')
                article = article.split(' ')
                self.corpora[corpus].extend(article)
