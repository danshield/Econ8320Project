from article import MyArticle
from gnews import GNews
import numpy as np
import pandas as pd

request = GNews(max_results=100)
articles = [MyArticle(request, a['title'], a['description'], a['published date'], a['url'], a['publisher']['title']) for a in request.get_news('+"Wagner group"')]

[a.Init() for a in articles]

merged = list()
[merged.extend(a.entities) for a in articles if (len(a.entities) > 0)]
unique = np.unique(merged)

columns = [e for e in unique if (merged.count(e) > (len(articles)*0.025))]

df = pd.DataFrame([(a.publisher, a.title, a.url, a.date) for a in articles], columns = ['Publisher','Title','URL','Date'])
for column in columns:
    list = []
    for a in articles:
        if (column in a.entities):
            list.append(1)
        else:
            list.append(0)
            
    df[column] = list

df.to_csv("Econ8320_Project.csv")
