from article import MyArticle
from gnews import GNews
import numpy as np
import pandas as pd

# Get list of articles to process
request = GNews(max_results=100)
articles = [MyArticle(request, a['title'], a['description'], a['published date'], a['url'], a['publisher']['title']) for a in request.get_news('+"Wagner group"')]

# Initialize all the objects
[a.Init() for a in articles]

# Create list of entities from all articles
merged = list()
[merged.extend(a.entities) for a in articles if (len(a.entities) > 0)]
unique = np.unique(merged)

# Create columns from the all but the least frequently used entities
columns = [e for e in unique if (merged.count(e) > (len(articles)*0.025))]

# Build the dataframe with articles as rows and entities and columns
df = pd.DataFrame([(a.publisher, a.title, a.url, a.date) for a in articles], columns = ['Publisher','Title','URL','Date'])
for column in columns:
    list = []
    for a in articles:
        if (column in a.entities):
            list.append(1)
        else:
            list.append(0)
            
    df[column] = list

# Save the results
df.to_csv("Econ8320_Project.csv")
