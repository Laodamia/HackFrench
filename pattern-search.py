import nltk
import spacy
import pandas as pd
import os
from pprint import pprint
from airtable import Airtable
from spacy.matcher import Matcher

nlp = spacy.load("fr_core_news_md")

base_key = '<base key>'
table_name = 'Key Sentences'
airtable = Airtable(base_key, table_name, api_key='<api key>')

#get all records from the airtable database
records = airtable.get_all()
   
#create a dataframe from airtable 
df = pd.DataFrame.from_records((r['fields'] for r in records))

#define patterns to search for
verb_det_noun = [{'POS':'VERB'}, {'POS':'DET'},{'POS':'NOUN'}]
adj_noun = [{'POS':'ADJ'}, {'POS':'NOUN'}]
adj_prep = [{'POS':'ADJ'}, {'POS':'PREP'}]
adv_adj_noun = [{'POS':'ADV'}, {'POS':'ADJ'},{'POS':'NOUN'}]

#functon to print all patterns
def pattern_search(pattern):
	for s in df['French']:
		#convert the French text to a doc
		doc = nlp(s) 

		#create matcher object
		matcher=Matcher(nlp.vocab)

		#add the required pattern
		matcher.add('chosen_pattern', None, pattern)
		for match_id, start, end in matcher(doc):
			span=doc[start:end]
			print(span.text)

pattern_search(verb_det_noun)