# Twitter Search Engine
A search engine that searches tweets related to **USA elections 2020** given a query.

## Installation
* Download the folder.

* Open the folder in command line promp and install the program. 
  ```
  $ pip install --editable .
  ```
  It will install the CLI programmed named **twitterSE**.

## Usage
### Execute a query

The result for the query will be displayed in the command line.
````
$ twitterSE --method [method] "query"
````
* **--method**: takes to values tf-idf or word2vec. Default: tf-idf

* **query**: query to search. Note: use brackets if query contains more than one word.

### Help
Run command `--help` to display help.
````
$ twitterSE --help
