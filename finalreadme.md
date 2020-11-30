# Twitter Search Engine
A search engine that searches tweets related to **USA elections 2020** given a query.

## Installation
* Download the folder.

* Open the folder in command line promp and install the program. **NOTE**: If you do not want to install it on your computer continue reading to see how to connect to the virtual enviroment.
  ```console
  foo@bar:~/SearchEngine$ pip install --editable .
  ```
  It will install the CLI programmed named **twitterSE**.

* Requirements
  * You can try to run it directly if you already have all Python modules used in practices installed.
  * Or you can connect to the **virtual enviroment**.
  ```console
  foo@bar:~/SearchEngine$ . venv/bin/activate 
  ```

## Usage
### Execute the program

This will initialize the program by constructing the index and the requirements for the choosen **method**.
````console
foo@bar:~/SearchEngine$ twitterSE --method [method]
````
* **--method**: takes to values tf-idf or word2vec. Default: tf-idf

### Search a query
Once the program has initialized you can run queries. The following will be displayed in command line.


### Help
Run command `--help` to display help.
````console
foo@bar:~/SearchEngine$ twitterSE --help
