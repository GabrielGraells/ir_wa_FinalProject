import pandas as pd
import re
import spacy
import string
from gensim.models import Doc2Vec
from nltk.stem import PorterStemmer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import pickle
import click
from parsers import Parsers


class doc2vec(object):
  def __init__(self, data):
    # Get data
    self.data_Final = data
    
    #Processed data
    self.data = pd.read_csv("data/d2v_processed.csv")
    
    #Init NLP
    self.nlp = spacy.load("en_core_web_sm",disable=["ner","parser"])
    self.nlp.max_length = 5000000
    
    #Load d2v model
    self.doc2vec_model = Doc2Vec.load("data/utils/d2v_model.kvmodel")
    
    #Load contractions
    self.contractions_dict = pickle.load(open("data/utils/contractions_dict.p","rb"))
    
    # Init parsers
    self.parsers = Parsers()
    
    # Load tag id
    self.tag_id = pickle.load(open("data/utils/tag_id.p","rb"))
    
    #Load id doc2vec
    self.id_doc2vec = pickle.load(open("data/utils/id_doc2vec.p","rb"))
    
    #Get query - run program
    self.get_query(self.id_doc2vec)
    
    
  def get_query(self, id_doc2vector):
    # Ask for query
    active = True
    while(active):
      click.echo("\n######################################################")
      click.echo("TYPE 'X' TO EXIT.")
      click.echo("Insert query:")
      query = input()
      click.echo("######################################################\n")
      
      if query == 'X' or query =='x':
        click.echo("Exiting...")
        active = False
      else:
        self.search(query, self.tag_id, self.id_doc2vec) 
        
    return 0
    
  def search(self, query, tag_id, id_doc2vector, topn= 20):
    """
    Search for tweets inputing a query and see displayed results.
    Arguments:
        id_doc2vector -- dic containing id:vec2doc pair - dic
        topn -- default: 20 - Top N result to display - int.

    """
    # Get ranked docs
    doc_query_sim = self.rank(query, self.tag_id)
    ids = doc_query_sim[:topn]
    
    click.echo("Results\n")
    
    for index, id in enumerate(ids):
        doc = self.data_Final[self.data_Final["id"] == id]
        tweet, date, author, retweets, favorites, url, hashtags = self.parsers.parser_tweet_results(doc)

        click.echo("______________________________________________________")
        click.echo(f"Tweet {index}")
        click.echo(f"\t·Author: {author}")
        click.echo(f"\t·Date: {date}")
        click.echo(f"\t·Tweet: {tweet}")
        click.echo(f"\t·Retweets: {retweets}")
        click.echo(f"\t·Favorites: {favorites}")
        click.echo(f"\t·Hashtags: {hashtags}")
        click.echo(f"\t·ULR: {url}")
        click.echo("______________________________________________________\n")
        
  def rank(self, query, tag_id):
      """
      Given a query preprocesses it, embeds it and return ordered dictionary of id:similarity_score
      pair.
      """
      # Pre-process query
      query = self.preprocessing(query)

      # Query vector
      q_vector = self.doc2vec_model.infer_vector(query.split())

      #Doc query similarity
      tag_sim = self.doc2vec_model.docvecs.most_similar([q_vector], topn=20)

      # Get Ids
      ids = [tag_id[id_[0]] for id_ in tag_sim] 
      
      return ids
      
      
  def expand_contractions(self, text, contractions_dict, contractions_re):
      """
      Given contraction find match and substitude
      """
      def replace(match):
          return contractions_dict[match.group(0)]
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
      text = self.expand_contractions(text,self.contractions_dict,contractions_re)
      text = self.clean_text(text)

      #Remove added spaces
      text = re.sub(" +"," ",text)
      text = text.strip()

      #Stop words and Lemmatizing
      text = ' '.join([token.lemma_ for token in list(self.nlp(text)) if (token.is_stop==False)])

      return text