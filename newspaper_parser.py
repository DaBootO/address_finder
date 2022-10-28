import newspaper
from newspaper import Article
import nltk

nltk.download('punkt')

with open('url_data.dat','r') as f:
    data = f.readlines()

cleaned_data = []

for l in data:
    cleaned_data.append(l.strip().split(',', 1))

for i in range(10):
    url = cleaned_data[i][0]
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    print(article.keywords)