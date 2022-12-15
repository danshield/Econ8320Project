from dateutil import parser
from gnews import GNews
from newspaper import Article
from newspaper import Config
from sutime import SUTime
import dateparser
import numpy as np
import os
import re
import spacy


class MyArticle():
    def __init__(self, news, title, description, date, url, publisher):
        self.news = news
        self.title = title
        self.description = description
        self.date = date
        self.url = url
        self.publisher = publisher

        self.dates = []
        self.entities = []
        self.doc = None    # Useful for debugging
        self.error = ""    # Useful for debugging
        
        self.sutime = self._init_parsers()

    
    # Set up the SUTime object
    def _init_parsers(self):
        jar_files = os.path.join(os.path.dirname(__file__), 'jars')
        return SUTime(jars=jar_files, mark_time_ranges=True)

        
    # String representation for debugging
    def __repr__(self):
        tmp = f'Title:        {self.title}\r\n'
        tmp += f'Description: {self.description}\r\n'
        tmp += f'Date:        {self.date}\r\n'
        tmp += f'URL:         {self.url}\r\n'
        tmp += f'Publisher:   {self.publisher}\r\n'

        return tmp

    
    # Clean up text when necessary
    def clean_text(self, e):
        tmp = e.text.replace('\n','').replace('the ', '').replace('The ', '')

        return tmp
    
    
    # Only select the labels we are interested in
    def filter_label(self, e):
        if (e.label_ == 'GPE'):
            return True
        elif (e.label_ == 'PERSON'):
            if (len(e.text.split(' ')) > 1): #include first and last names
                return True
        else:
            return False
        
    
    # Get the list of DATE entities
    def get_dates(self, str):
        # Get the dates
        dates = self.sutime.parse(str)
        dates = [x['value'] for x in dates]
        
        # Put them in the string format we need
        dtFormat = '\d{4}-\d{2}-\d{2}'
        return  [dateparser.parse(d).strftime('%Y-%m-%d') for d in dates if (re.search(dtFormat, d))]
        

    # Download, parse, and collect entities from article text
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