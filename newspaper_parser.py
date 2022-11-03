import pickle
from newspaper import Article
from tqdm import trange
import gensim
from gensim import corpora

# nltk import
# modules for lemmatizing the tokens
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

# spacy import
# modules for tokenizing sentences
import spacy
nlp = spacy.load("de_core_news_sm")
from spacy.lang.de import German
lang_parser = German()

def tokenize(text):
    lda_tokens = []
    tokens = lang_parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    # lemmatize all tokens which are longer than 4 characters and NOT a stop word
    tokens = [get_lemma(token) for token in tokens if len(token) > 4 and token not in de_stop]
    return tokens

# define stopwords
de_stop = set(nltk.corpus.stopwords.words('german'))

with open('url_data.dat','r') as f:
    data = f.readlines()

cleaned_data = [l.strip().split(',', 1) for l in data]

text_data = []

for i in trange(10):
    url = cleaned_data[i][0]
    article = Article(url)
    article.download()
    article.parse()
    text_data.append(prepare_text_for_lda(article.text))
    # print(article.text)
    # print(prepare_text_for_lda(article.text))
    # article.nlp()
    # print(article.keywords)

# creating a dictionary and transforming DOCument to Bag-Of-Words (BOW)
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

# pickling and dumping data for later use
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

NUM_TOPICS = 1
ldamodel = gensim.models.ldamodel.LdaModel(
    corpus,
    num_topics=NUM_TOPICS,
    id2word=dictionary,
    passes=15)

ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=10)

for topic in topics:
    print(topic)