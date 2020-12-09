import click
from searchengine import SearchEngine

@click.command()
@click.option("--method", default="tf-idf",
            help = "Method used to rank -- default:'tf-idf' -- values: ['tf-idf', 'word2vec', 'doc2vec'] ")
def cli(method):
    """
    A search engine that searches tweets related to USA elections 2020 given a query.
    """
    
    se = SearchEngine(method)
    
    return 0