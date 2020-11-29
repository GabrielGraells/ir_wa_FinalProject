# IR_WA_FinalProject

## 1. Data Collection [X]
* ### Twitter Scrapper [X]
	* News Media Account [X]
	* Tags [X]
	* Political Agents [X]

## 2. Build the Search Engine [ ]
* ### Prepocessing [X]
	* Removing stop-words [X]
	* Removing punctation [X]
	* Stemming [X]
	* Anonymize users IDs [X]
 
 * ### Inverted-index [X]
 
 **Important !** : Do not only use the terms in the tweet. Other fields in tweet could be use for search (metada).
 
  {
	   Term_id_1: [document_1, document_2, document_4],
	   Term_id_2: [document_1, document_3, document_5, document_6], 
	   etc...
  }
  
  **Query Return**: [tweet, **username**, date, **hashtags**, like, retweets, urls]
  
* ### Ranking Score
	* **TDF-ID + cosine-sim** [X]
	* **Your-score + cosine-sim** [ ]
	
**Return the top-20 docs given query**

* ### Command line program [X]
* ### Report [ ]
	* Output Analysis - Notebook [ ]
	* Output Diversification - Notebook [ ]
	* Link Analysis - Notebook[ ]
	* Section 1 - Data collection [ ]
	* Section 2 - Search Engine [ ]
	* Section 3 - RQs [ ]

* ### Github Repository [ ]
