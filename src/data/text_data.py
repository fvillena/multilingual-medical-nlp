import os
import json
import hashlib
import collections
import operator
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.fr import French
from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result
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
    def load_files(self, restrict_documents=0):
        self.corpora = {language:[] for language in self.files.keys()}
        for corpus,files in self.files.items():
            if restrict_documents:
                if len(files) > restrict_documents:
                    files = files[:restrict_documents]
            for document_file in files:
                with open(document_file, 'r', encoding='utf-8') as f:
                    article = f.read()
                article = article.replace('\n',' ')
                article = article.split(' ')
                self.corpora[corpus].append(article)
    def tfidf_analysis(self):
        self.corpora_idf = {language:[] for language in self.files.keys()}
        for language in self.corpora_idf:
            corpus = [' '.join(document) for document in self.corpora[language]]
            vectorizer = TfidfVectorizer()
            vectorizer.fit(corpus)
            vocab = vectorizer.get_feature_names()
            idf = vectorizer.idf_
            word_idf = list(zip(vocab,idf))
            word_idf = sorted(word_idf, key=lambda x: x[1], reverse=True)
            self.corpora_idf[language] = word_idf
    def tf_analysis(self):
        self.corpora_tf = {language:[] for language in self.files.keys()}
        for language in self.corpora_tf:
            counter = Counter(flatten(self.corpora[language]))
            self.corpora_tf[language] = counter.most_common()
    def generate_report(self):
        self.report = {language:{} for language in self.files.keys()}
        for language in self.report.keys():
            self.report[language]['n_documents'] = len(self.corpora[language])
            self.report[language]['n_words'] = len(flatten(self.corpora[language]))
            self.report[language]['vocab_size'] = len(set(flatten(self.corpora[language])))
            try: self.report[language]['idf'] = self.corpora_idf[language][:100]
            except: pass
            try: self.report[language]['tf'] = self.corpora_tf[language][:100]
            except: pass
        return self.report

class MyTfidfAnalyzer:
    def __init__(self, tf_file_location, idf_file_location):
        with open(tf_file_location, 'r', encoding='utf-8') as f:
            self.tf = json.load(f)
        with open(idf_file_location, 'r', encoding='utf-8') as f:
            self.idf = json.load(f)
        self.tf = {corpus:dict(data) for corpus,data in self.tf.items()}
        self.idf = {corpus:dict(data) for corpus,data in self.idf.items()}
    def analyze(self):
        self.tfidf = {
            language:sorted({
                word:self.tf[language][word]*(self.idf[language][word] - 1) for word in self.tf[language] if word in self.idf[language]
                }.items(), key=operator.itemgetter(1), reverse=True) for language in self.idf
            }
        