import pandas as pd
import re
import spacy
from parsers import Parsers
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import click

class word2vec(object):
  
  def __init__(self, data):
    # Store data
    self.data_Final = data
    
    # Read prepocessed data
    self.data = pd.read_csv("data/w2v_processed.csv")
    
    # Init NLP
    self.nlp = spacy.load("en_core_web_sm",disable=["ner","parser"])
    self.nlp.max_length = 5000000
    
    # Load w2v model
    self.w2v_model = KeyedVectors.load("data/utils/w2v_model.kvmodel")
    
    # Load contractions
    self.contractions_dict = pickle.load(open("data/utils/contractions_dict.p","rb"))
    
    # Init parser
    self.parsers = Parsers()
    
    # Load id_doc2vector
    self.id_doc2vector = pickle.load(open("data/utils/id_doc2vec.p", "rb"))
    
    # Get query
    self.get_query(self.id_doc2vector)
    
  def get_query(self, id_doc2vector):
    # Ask for query
    active = True
    while(active):
      click.echo("######################################################")
      click.echo("TYPE 'X' TO EXIT.")
      click.echo("Insert query:")
      query = input()
      click.echo("######################################################\n")
      
      if query == 'X' or query =='x':
        click.echo("Exiting...")
        active = False
      else:
        self.search(query, self.id_doc2vector) 
        
    return 0
    
    
    
  def expand_contractions(self, text, contractions_re):
    """
      Given contraction find match and substitude
    """
    def replace(match):
        return self.contractions_dict[match.group(0)]
    return contractions_re.sub(replace,text)
    
    
  def clean_text(self, text):
    """
    * Remove words with digits
    * Replace newline characters with space
    * Remove URLS
    * Replace non english chars with space
    """
    # Remove digits
    text=re.sub('\w*\d\w*','', text)

    # Remove new Line chars
    text=re.sub('\n',' ',text)

    #Remove links
    text=re.sub(r"http\S+", "", text)

    #Replace non-english chars
    text=re.sub('[^a-z]',' ',text)

    return text
    
  
  def preprocessing(self, text):
    """
    Given a pandas dataframe apply preprocessing techinques
        * Lowercase the text
        * Expand Contractions
        * Clean the text
        * Remove Stopwords
        * Lemmatize words
    """
    # Lower case
    text = text.lower()

    # Regular expression for finding contractions
    contractions_re=re.compile('(%s)' % '|'.join(self.contractions_dict.keys()))

    #Expand contractions
    text = self.expand_contractions(text,contractions_re)
    text = self.clean_text(text)

    #Remove added spaces
    text = re.sub(" +"," ",text)
    text = text.strip()

    #Stop words and Lemmatizing
    text = ' '.join([token.lemma_ for token in list(self.nlp(text)) if (token.is_stop==False)])

    return text
    
  
  def embedding_w2v(self, doc_tokens):
    """
    Returns vector representation of a string
    """
    embeddings = []
    if len(doc_tokens)<1:
        return np.zeros(100)
    else:
        for t in doc_tokens:
            if t in self.w2v_model.wv.vocab:
                embeddings.append(self.w2v_model.wv.word_vec(t))
            else:
                embeddings.append(np.random.rand(100))

    return np.mean(embeddings, axis = 0)
    
  
  def w2v_collection(self, data):
    """
    Given a collection of documents returns the pair id:vector where the vector is
    the embedding representation of the doc.
    """
    id_doc2v = {}
    for id, text in zip(data["id"].values, data["full_text"]):
        id_doc2v[id] = self.embedding_w2v(text)

    return id_doc2v
    
    
  def rank(self, query, id_doc2vec):
    """
    Given a query preprocesses it, embeds it and return ordered dictionary of id:similarity_score
    pair.
    """
    # Pre-process query
    query = self.preprocessing(query)

    # Query vector
    q_vector = self.embedding_w2v(query.split())

    #Doc query similarity
    doc_query_sim = {k: cosine_similarity(np.array(v).reshape(1,-1),np.array(q_vector).reshape(1,-1)) for k,v in id_doc2vec.items()}

    # Sort
    doc_query_sim = {k: v for k, v in sorted(doc_query_sim.items(), key=lambda item: item[1], reverse = True)}

    return doc_query_sim

  def search(self, query, id_doc2vector, topn= 20):
    """
    Search for tweets inputing a query and see displayed results.
    Arguments:
    id_doc2vector: dic containing id:vec2doc pair - dic
    topn -- default: 20 - Top N result to display - int.

    """
    # Get ranked docs
    doc_query_sim = self.rank(query, id_doc2vector)
    ids = list(doc_query_sim.keys())[:topn]
    
    click.echo("Results\n")
    
    for index, id in enumerate(ids):
        doc = self.data_Final[self.data_Final["id"] == id]
        tweet, date, author, retweets, favorites, url, hashtags = self.parsers.parser_tweet_results(doc)
  
        print("______________________________________________________")
        print(f"Tweet {index}")
        print(f"\t·Author: {author}")
        print(f"\t·Date: {date}")
        print(f"\t·Tweet: {tweet}")
        print(f"\t·Retweets: {retweets}")
        print(f"\t·Favorites: {favorites}")
        print(f"\t·Hashtags: {hashtags}")
        print(f"\t·URL: {url}")
        print("______________________________________________________\n")
