from gnews import GNews
from article import Article
import pandas as pd

request = GNews(max_results=100)
articles = [Article(request, a['title'], a['description'], a['published date'], a['url'], a['publisher']['title']) for a in request.get_news('+"Wagner group"')]

[a.Init() for a in articles]

merged = list()
[merged.extend(a.entities) for a in articles]

unique = set(merged)

df = pd.DataFrame(merged)
df2 = df.groupby('value').count()
df2.sort_values(by='type', ascending=False)

