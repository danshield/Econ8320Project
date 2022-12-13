import re
from gnews import GNews
import spacy
from dateutil import parser
from newspaper import Config
from newspaper import Article
import os
from sutime import SUTime
import dateparser
import numpy as np


class MyArticle():
    def __init__(self, news, title, description, date, url, publisher):
        self.news = news
        self.title = title
        self.description = description
        self.date = date
        self.url = url
        self.publisher = publisher

        self.entities = []
        self.doc = None
        self.error = ""
        self.dates = []
        
        self.sutime = self._init_parsers()

    def _init_parsers(self):
        jar_files = os.path.join(os.path.dirname(__file__), 'jars')
        return SUTime(jars=jar_files, mark_time_ranges=True)
        
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
#        elif (e.label_ == 'DATE'):
#            if (' ' in e.text or len(e.text) > 4):
#                return True
        else:
            return False
        
    def get_dates(self, str):
        dates = self.sutime.parse(str)
        dates = [x['value'] for x in dates]
        
        dtFormat = '\d{4}-\d{2}-\d{2}'
        return  [dateparser.parse(d).isoformat() for d in dates if (re.search(dtFormat, d))]
        

    def Init(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        config = Config()
        config.browser_user_agent = user_agent

        try:
            npArticle = Article(self.url, config=config)
            npArticle.download()
            npArticle.parse()

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(npArticle.text)
            entities = [self.clean_text(e) for e in doc.ents if (self.filter_label(e))]

            self.entities = np.unique(entities).tolist()
            self.entities.extend(np.unique(self.get_dates(doc.text)).tolist())
            self.doc = doc
        except:
            self.error = f"Failing at {self.url}"