# ir_wa_FinalProject

# Index
## 1. Data Collection [ ]
  * ### Twitter Scrapper [ ]
  **Keywords**: [#election #trump #vote #democrats #donaldtrump #voteblue #resist #biden #politics #coronavirus #republican #joebiden #liberal #america #usa #democrat #guncontrol #trumpsucks #bluewave #berniesanders #impotus #bernie #trumptreason]

## 2. Build the Search Engine [ ]
 * ### Prepocessing [ ]
  * Removing stop-words [ ]
  * Removing punctation [ ]
  * Stemming [ ]
  * Anonymize users IDs [ ]
 * ### Inverted-index [ ]
 Important ! : Do not only use the terms in the tweet. Other fields in tweet could be use for search (metada).
  {
	   Term_id_1: [document_1, document_2, document_4],
	   Term_id_2: [document_1, document_3, document_5, document_6], 
	   etc...
  }
