import os
from pprint import pprint
from airtable import Airtable
import pandas as pd

base_key = '<BASE KEY HERE>'
table_name = 'Key Sentences'
airtable = Airtable(base_key, table_name, api_key='<API KEY HERE>')

#get all records from teh airtable database
records = airtable.get_all()

#create a dataframe from airtable
df = pd.DataFrame.from_records((r['fields'] for r in records))

#change id numbers to int
df['Video ID'] = df['Video ID'].astype(int)
df['Line ID'] = df['Line ID'].astype(int)


def create_srt(video_id):
	#create a new df filtered by video ID and sort by line ID
	filtered_df = df[df['Video ID']==video_id].sort_values(by='Line ID')

	# all_lines= []
	f_frsf = open("[FR-SF]subs_dialogue_{}.srt".format(video_id), "w")
	#add line number in range ofthe length of all records in a group
	for n in range(0,len(filtered_df)):
		row = filtered_df.iloc[n]
		fr = row[u'French']
		en = row[u'English (manual)']
		simpl_f = row[u'Line sunpleman fransé']
		s_time = row['Time Start']
		e_time = row['Time Stop']

		# print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		# one_line = print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		one_line = """{}
{} --> {}
{}
{}
""".format(n,s_time,e_time,fr,simpl_f)

		print(one_line, file=f_frsf)
	f_frsf.close()
	f_en = open("[EN]subs_dialogue_{}.srt".format(video_id), "w")
	#add line number in range ofthe length of all records in a group
	for n in range(0,len(filtered_df)):
		row = filtered_df.iloc[n]
		fr = row[u'French']
		en = row[u'English (manual)']
		simpl_f = row[u'Line sunpleman fransé']
		s_time = row['Time Start']
		e_time = row['Time Stop']

		# print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		# one_line = print(n, '\n', s_time, '-->', e_time, '\n', fr,'\n', en, '\n', simpl_f,'')
		one_line = """{}
{} --> {}
{}
""".format(n,s_time,e_time,en)

		print(one_line, file=f_en)
	f_en.close()





#test
vid_num = 6
create_srt(vid_num)
