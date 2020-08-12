import nltk
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
import numpy as np
import os
from pprint import pprint
from airtable import Airtable
import pandas as pd
import string

nlp = spacy.load("fr_core_news_md")

base_key = '<base key>'
table_name = 'Key Sentences'
airtable = Airtable(base_key, table_name, api_key='<api key>')

#get all records from the airtable database
records = airtable.get_all()
   
#create a dataframe from airtable 
df = pd.DataFrame.from_records((r['fields'] for r in records))

#create an empty df with relevant columns
new_df = pd.DataFrame(columns=['sentence','word', 'POS', 'tag','tag_explain','dep','lemma','entity','entity_label'])

#iterate through the series
for s in df['French']:
	#nlp the French
 	doc = nlp(s) 
 	#create a new df with filling in the columns with required attributes
 	for token in doc:
 		new_df = new_df.append({'sentence': s, 
 			'word': token.text, 
 			'POS' : token.pos_,
 			'tag' : token.tag_,
 			'tag_explain': spacy.explain(token.tag_),
 			'dep' : token.dep_,
 			'lemma': token.lemma_
 			},
 			ignore_index=True)

	for ent in doc.ents:
 		new_df = new_df.append({'entity': ent.text, 'entity_label': ent.label_},ignore_index=True)

print(new_df.head())