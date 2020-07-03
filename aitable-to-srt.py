import os
from pprint import pprint
from airtable import Airtable
import pandas as pd

base_key = input('base key: ')
table_name = 'Key Sentences'

api_key = input('api key: ')
key_sentences = Airtable('app3qY4PvmhbRYcfj', 'Key Sentences', api_key = api_key)

video_id = input("The video ID:  ")

def create_srt(video_id):
	formula = '{Video ID}='+str(video_id)
	#create a new df filtered by video ID and sort by line ID
	# filtered_df = df[df['Video ID']==video_id].sort_values(by='Line ID')
	sentences = key_sentences.get_all(formula=formula,sort=[('Line ID','asc')])

	# all_lines= []
	f_frsf = open("[FR-SF]subs_dialogue_{}.srt".format(video_id), "w")
	#add line number in range ofthe length of all records in a group
	for i in range(len(sentences)):
		fr = sentences[i]['fields']['French']
		en = sentences[i]['fields']['English (manual)']
		simpl_f = sentences[i]['fields']['Line sunpleman fransé']
		s_time = sentences[i]['fields']['Time Start']
		e_time = sentences[i]['fields']['Time Stop']

		# print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		# one_line = print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		one_line = """{}
{} --> {}
{}
{}
""".format(i,s_time,e_time,fr,simpl_f)

		print(one_line, file=f_frsf)
	f_frsf.close()
	f_en = open("[EN]subs_dialogue_{}.srt".format(video_id), "w")
	#add line number in range ofthe length of all records in a group
	for i in range(len(sentences)):
		fr = sentences[i]['fields']['French']
		en = sentences[i]['fields']['English (manual)']
		simpl_f = sentences[i]['fields']['Line sunpleman fransé']
		s_time = sentences[i]['fields']['Time Start']
		e_time = sentences[i]['fields']['Time Stop']

		# print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		# one_line = print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		one_line = """{}
{} --> {}
{}
""".format(i,s_time,e_time,en)

		print(one_line, file=f_en)
	f_en.close()





#test

create_srt(video_id)
