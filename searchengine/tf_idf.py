import pandas as pd
import click
import collections
from parsers import Parsers
from collections import defaultdict
from array import array
import numpy as np
import pickle


class tf_idf(object):
  
  def __init__(self, data):
    # Load data
    self.data = data
    
    # Parser
    self.parsers = Parsers()
    
    # Init tf-idf
    click.echo("Creating: index and tf-idf")
    self.index, self.tf, self.df, self.idf = self.load_index_tfidf()
    click.echo("Done.\n")
    
    #Ask for query
    self.get_query()
    
    
    
  def get_query(self):
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
        self.search(query, self.index, self.idf, self.tf) 
        
    return 0
     
  def load_index_tfidf(self):
    """
      Loads the preprocesed returns:
      Returns:
        index --  inverted list "term": [["id",[pos1,pos1,..]].
        tf -- normalized term frequency per doc 
        df -- document frequency per term
        idf -- inversed docuemnt frequency
    """

    index = pickle.load(open("data/utils/index.p", "rb"))

    # Term freq of terms in tweets      
    tf = pickle.load(open("data/utils/tf.p", "rb"))

    # Tweet freq of term in corpus
    df = pickle.load(open("data/utils/df.p", "rb"))
    
    # Inverse df
    idf = pickle.load(open("data/utils/idf.p", "rb"))
  
    return index, tf, df, idf
        
  def rankDocuments(self, terms, docs, index, idf, tf):
    """
    Computes ranking given query and collection of tweets.

    Arguments:
      terms -- query - str.
      docs -- ID list of docs - list.
      index -- invertex index. - dict
      idf -- inverse document frequency - dict
      tf -- term frequency - dict
    Returns:
      resultDocs -- Ordered list of matching docs based on cosine-sim - list
    """

    # Dict with vector per docID
    docVectors = defaultdict(lambda: [0]*len(terms))

    # Vector per query
    queryVector = [0]*len(terms)

    # TF of query
    query_terms_count = collections.Counter(terms)
 
    # Norm query
    query_norm = np.linalg.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):
      # Check if term exist in collection
      if term not in index:
        continue

      # Score per term-query
      queryVector[termIndex] = query_terms_count[term]/query_norm * idf[term]

      for docIndex, (doc,postings) in enumerate(index[term]):
        # check if IDdoc is in list of IDdocs containg term
        if doc in docs:
          # Score per term-doc
          docVectors[doc][termIndex] = tf[term][docIndex] * idf[term]

    #Cosine similarity query-doc
    docScores = [[np.dot(curDocVec, queryVector), doc] for doc, curDocVec in docVectors.items()]

    #Sort by descending similarity
    docScores.sort(reverse=True)

    #Get IDs
    resultDocs = [x[1] for x in docScores]

    return resultDocs
  
  def search_tf_idf(self, query, index, idf, tf, topn):
    """
  Preprocess query and find docs with words in query
  Arguments:
    query -- query - str.
    index -- inverted index - dict
    idf -- inverse document frequency - dict
    tf -- term frequency - dict
    topn -- N top ranked docs to be returned - int
  Returns
    ranked_docs -- list of topn docs ranked by cosine-sim - list
    """
    # Preprocess query
    query = self.parsers.getTerms(query)
 
    # Init set of docs with terms in query
    docs = set()

    for term in query:
      try:
        # Get IDs of docs with term
        termDocs = [posting[0] for posting in index[term]]
      
        # Add new docsID
        docs = docs.union(termDocs)
    
      except:
        pass
    
    docs = list(docs)

    # Rank docs with rankDocuments
    ranked_docs = self.rankDocuments(query, docs, index, idf, tf)
    ranked_docs = ranked_docs[:topn]

    return ranked_docs
  
  def search(self, query, index, idf, tf, topn = 20):
    """
  Search for tweets inputing a query and see displayed results.
  Arguments:
    index -- inverted index - dict
    idf -- inverse document frequency - dict.
    tf -- term frequency - dict.
    topn -- default: 20 - Top N result to display - int.
    """
  
    # Get topn docs
    ranked_docs = self.search_tf_idf(query, index, idf, tf, topn)

    if len(ranked_docs) == 0:
      click.echo("No results found !\n")
      return -1
  
    click.echo("Results\n")

    for index, id in enumerate(ranked_docs):
      # Get tweet corresponding to id
      doc = self.data[self.data['id'] == id]
      tweet, date, author, retweets, favorites, url, hashtags = self.parsers.parser_tweet_results(doc)
    
      click.echo("______________________________________________________")
      click.echo(f"Tweet {index}")
      click.echo(f"\t·Author: {author}")
      click.echo(f"\t·Date: {date}")
      click.echo(f"\t·Tweet: {tweet}")
      click.echo(f"\t·Retweets: {retweets}")
      click.echo(f"\t·Favorites: {favorites}")
      click.echo(f"\t·Hashtags: {hashtags}")
      click.echo(f"\t·URL: {url}")
      click.echo("______________________________________________________\n")