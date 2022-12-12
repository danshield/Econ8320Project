from gnews import GNews
import spacy
from dateutil import parser

class Article():
    def __init__(self, news, title, description, date, url, publisher):
        self.news = news
        self.title = title
        self.description = description
        self.date = date
        self.url = url
        self.publisher = publisher

        self.entities = []
        self.doc = None

    def __repr__(self):
        tmp = f'Title:        {self.title}\r\n'
        tmp += f'Description: {self.description}\r\n'
        tmp += f'Date:        {self.date}\r\n'
        tmp += f'URL:         {self.url}\r\n'
        tmp += f'Publisher:   {self.publisher}\r\n'

        return tmp

    
    def clean_text(self, e):
        tmp = e.text.replace('\n','')
        tmp = tmp.replace('the ', '')

        return tmp
    
    
    def filter_label(self, e):
        if (e.label_ == 'GPE'):
            return True
        elif (e.label_ == 'PERSON'):
            if (len(e.label_.split(' ')) > 1):
                return True
        elif (e.label_ == 'DATE'):
            if (' ' in e.text or len(e.text) > 4):
                return True
        else:
            return False
        
        
    def Init(self):
        try:
            npArticle = self.news.get_full_article(self.url)
            npArticle.parse()

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(npArticle.text)
            entities = [(self.clean_text(e), e.label_) for e in doc.ents if (self.filter_label(e))]
    #        entities = [(e.text.replace('\n',''), e.label_) for e in doc.ents if ((e.label_ in ['GPE', 'PERSON']) or
    #                                                                              ((e.label_ == 'DATE') and ((' ' in e.text) or
    #                                                                                                         (len(e.text) > 4))))]
            self.entities = set(entities)                                                                                                
            self.doc = doc
        except:
            print(f"Failing at {self.url}")