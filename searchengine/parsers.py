from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import nltk

class Parsers:
  
  def __init__(self):
    nltk.download('stopwords')
    # Init stemming and stopwords
    self.stemming = PorterStemmer()
    self.STOPWORDS = set(stopwords.words("english"))
    
  
  def getTerms(self, terms):

    """
    Preprocess step for tweet.
      1. transform all text in lowercase
      2. Tokenize by transforming string to list
      3. Remove stopwords
      4. Apply stemming, simplify word to root word.

    Argument:
      terms -- string (text)

    Returns:
      terms -- a list of preprocessed tokens corresponding to the input tweet 
    """

    # Transform into lower case
    terms = terms.lower() 

    # Remove punctuation
    terms = terms.translate(str.maketrans("","", string.punctuation))

    # Tokenize
    terms = terms.split()

    # Remove stop words
    terms = [t for t in terms if t not in self.STOPWORDS]

    #Stemming
    terms = [self.stemming.stem(t) for t in terms]

    # Remove http links found in tweets last term
    try:
      if terms[-1][:4] == "http":
        terms = terms[:-1]
    except:
      pass
      
    return terms
  
  
  def parser_tweet_results(self, doc):
    """
  Given a Pandas dataframe row formates the information por display
  Arguments:
    docs -- pandas dataframe with unique row with tweet info.
  Returns:
    tweet -- text tweet - str
    authors -- user name of tweet - str
    date -- of publication -- str
    retweets -- count of retweets - str
    favorites -- count of favourites - str
    """
    # Tweet
    tweet = str(doc["full_text"].values)
    tweet = tweet.replace("'","")
    tweet = tweet.replace("[","")
    tweet = tweet.replace("]","")

    # Author
    author = str(doc["user.name"].values)
    author = author.replace("[","")
    author = author.replace("]","")

    # Date
    date = str(doc["created_at"].values)
    date = date.replace("[","")
    date = date.replace("]","")
    date = date.replace("'","")

    # Retweets
    retweets = str(doc["retweet_count"].values)
    retweets = retweets.replace("[","")
    retweets = retweets.replace("]","")

    # Favorites
    favorites = str(doc["favorite_count"].values)
    favorites = favorites.replace("[","")
    favorites = favorites.replace("]","")

    # URL
    id = str(doc["id"].values)
    id = id.replace("[","")
    id = id.replace("]","")
    url = f"https://twitter.com/twitter/statuses/{id}"

    #Hashtags
    hashtags = str(doc["entities.hashtags"].values)

    return tweet, date, author, retweets, favorites, url, hashtags