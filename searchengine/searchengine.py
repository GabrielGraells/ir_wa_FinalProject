import pandas as pd
import click
from tf_idf import tf_idf
from word2vec import word2vec
from doc2vec import doc2vec


class SearchEngine(object):
    
  def __init__(self, method):
    """ Loads data. Creates index, tf and idf for collection."""
    
    self.method = method
    
    # Check if method is valid
    if self.method not in ["tf-idf","word2vec","doc2vec"]:
      print("\nERROR: Method not valid!\n")
      return None
    
    # Load data
    click.echo("\nLoading Data...")
    self.data = pd.read_csv("data/final_Tweets.csv")
    self.numDocs = len(self.data)
    click.echo(f"Total of {self.numDocs} tweets -- Done loading.\n")
    
    # Selector given method
    self.selector(self.method)
    
    
  def selector(self, method):
    """
    Selector for the choosen method.
    """
    #Init given method
    # TF-IDF
    if self.method == "tf-idf":
      self.tf_idf = tf_idf(self.data)      
     
    # Word to vec      
    elif self.method == "word2vec":
      self.word2vec = word2vec(self.data)
    
    elif self.method == "doc2vec":
      self.doc2vec = doc2vec(self.data)
    
