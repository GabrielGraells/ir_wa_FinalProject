# Twitter Search Engine
A search engine that searches tweets related to **USA elections 2020** given a query.

### Installation
* Download the folder *SearchEngine*.

* Open the folder in command line promp and install the program. **NOTE**: If you do not want to install it on your computer continue reading to see how to connect to the virtual enviroment.
  ```console
  foo@bar:~/SearchEngine$ pip install --editable .
  ```
  It will install the CLI programmed named **twitterSE**.

* Requirements
  * You can try to execute it directly if you already have all Python modules used in practices installed.
  * You can also connect to the **virtual enviroment**. **You can download the virtual enviroment from this** [link.](https://drive.google.com/file/d/198Qk3eSxJ2LyHh0sVaxUBFqFesWj0RrC/view?usp=sharing)
  ```console
  foo@bar:~/SearchEngine$ . venv/bin/activate 
  ```

### Usage
#### Execute the program

This will initialize the program by constructing the index and the requirements for the choosen **method**.
````console
foo@bar:~/SearchEngine$ twitterSE --method [method]
````
* **--method**: Ranking method. Takes values tf-idf or word2vec. Default: tf-idf

#### Search a query
Once the program has initialized you can run queries. The following will be displayed in command line.
```
######################################################
TYPE 'X' TO EXIT.
Insert query:
[your_query]
######################################################
```


#### Help
Run command `--help` to display help.
````console
foo@bar:~/SearchEngine$ twitterSE --help
````

## Contect in Repository
```
├── ir_wa_FinalProject
    ├── notebook
    │   ├── RQ1.ipynb
    |   ├── RQ2.ipynb
    |   ├── RQ3.ipynb
    |   ├── scrapper
    |   |   ├── TwitterScrapper.ipynb
    |   ├── searchengines_notebooks
    |       ├── TF-IDF.ipynb
    |       ├── doc2vec.ipynb
    |       ├── word2vec.ipynb
    ├── other_outputs
    |   ├── RQ1_results_DOC2VEC.csv
    |   ├── RQ1_results_TF_IDF.csv
    |   ├── RQ2_WITH.csv
    |   ├── RQ2_WITHOUT.csv
    |   ├── screenshoots
    |       ├── doc2vec.png
    |       ├── tf-idf.png
    ├── searchengine
    |   ├── venv
    |   ├── ...
    ├── README.md
```
