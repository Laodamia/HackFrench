from airtable import Airtable
import pandas as pd
import genanki
import random
from datetime import datetime
import time
import moviepy
from gtts import gTTS
from pathlib import Path

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def srt_time_to_sec(time_srt):
  td = datetime.strptime(time_srt,'%H:%M:%S,%f') - datetime(1900,1,1)
  return td.total_seconds()

api_key = input("Paste your API Key here:  ")
video_name = Path(input("copy paste the name of the video to use (should be in the same folder as this script):  "))
video_id = input("The video ID:  ")

# at = airtable.Airtable('app3qY4PvmhbRYcfj', api_key)

# key_sentences = at.get('Key Sentences')
key_sentences = Airtable('app3qY4PvmhbRYcfj', 'Key Sentences', api_key = api_key)
# df_ks = pd.DataFrame([record['fields'] for record in key_sentences.get_all(sort=[('Line ID','asc')])])

# video = df_ks.loc[df_ks['Video ID'] == str(video_id)]


# key_phrases = at.get('Key phrases')
key_phrases = Airtable('app3qY4PvmhbRYcfj', 'Key phrases', api_key = api_key)
# df_kp = pd.DataFrame([record['fields'] for record in key_phrases.get_all(sort=[('Line ID','asc')])])
# print(df_kp)

# key_words = at.get('Key words')

key_words = Airtable('app3qY4PvmhbRYcfj', 'Key words', api_key = api_key)
# df_kw = pd.DataFrame([record['fields'] for record in key_words.get_all(sort=[('Line ID','asc')])])
# print(df_kw)


# Split the video into short videos
# Split the video into short audios

video_recognition = genanki.Model(
  1851172070,
  'Video Recognition',
  css="""
  .card {
 font-family: futura;
 font-size: 20px;
 text-align: center;
 color: #373f51;
 background-color: #eeebd0;
}

.media {
 margin: 2px;
}
  """,
  fields=[
    {'name': 'Video ID'},
    {'name': 'Line ID'},
    {'name': 'Video Media'},
    {'name': 'French'},
    {'name': 'English'},
    {'name': 'Sunpleman Fransé'},
    {'name': 'Phonetic IPA'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'css': '',
      'qfmt': '<div class="media">{{Video Media}}</div>',
      'afmt': '{{FrontSide}}<hr id=answer><div style="font-family: Futura; font-size: 20px;">{{English}}</div><div style= font-family: Futura; font-size: 15px;>{{French}}</div><br/><div style= "color:#ee6c4d; font-family: Arial; font-size: 30px;">{{Sunpleman Fransé}}</div><br/><div style="font-family: Arial; font-size: 20px;">{{Phonetic IPA}}</div><br/><div style= "color:#00afb9; font-family: Futura; font-size: 10px;">© Hack French with Tom</div>',
    },
  ])

build_up_model = genanki.Model(
  1789984366,
  'Build Up Model',
  css="""
  .card {
 font-family: futura;
 font-size: 20px;
 text-align: center;
 color: #373f51;
 background-color: #eeebd0;
}

.media {
 margin: 2px;
}
  """,
  fields=[
    {'name': 'Video ID'},
    {'name': 'Line ID'},
    {'name': 'English'},
    {'name': 'French'},
    {'name': 'Sunpleman Fransé'},
    {'name': 'Phonetic IPA'},
    {'name': 'TTS'},
    {'name': 'audio'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'css': '',
      'qfmt': '<div style="font-family: Futura; font-size: 20px;">{{English}}</div>',
      'afmt': '{{FrontSide}}<hr id=answer><div style="font-family: Futura; font-size: 20px;"></div>{{audio}}<div style= font-family: Futura; font-size: 15px;>{{French}}</div><br/><div style= "color:#ee6c4d; font-family: Arial; font-size: 30px;">{{Sunpleman Fransé}}</div><br/><div style="font-family: Arial; font-size: 20px;">{{Phonetic IPA}}</div><br/><div style= "color:#00afb9; font-family: Futura; font-size: 10px;">© Hack French with Tom</div>',
    },
  ])

# new_note = genanki.Note(
#   model=build_up_model,
#   fields=['6','1','Hello world','Bonjour le monde','bonjour le mond','bõjfe','bonjour le monde','/df_ks/df_ks']
# )

# deck = genanki.Deck(2089870830, 'css deck')
# deck.add_note(new_note)
# genanki.Package(deck).write_to_file('css.apkg')

def generate_anki_deck(selected_video,required_video_file):
  deck_id = random.randrange(1 << 30, 1 << 31)
  video_deck = genanki.Deck(deck_id, 'flashcards deck video {}'.format(selected_video))
  package = genanki.Package(video_deck)
  formula = '{Video ID}='+str(selected_video)
  sentences = key_sentences.get_all(formula=formula,sort=[('Line ID','asc')])
  for i in range(len(sentences)):
    print('Sentence',i)
    try:
      for word_id in sentences[i]['fields']['Key Words']:
        word = key_words.get(word_id)
        print(word['fields']['French'])
        tts = gTTS(word['fields']['TTS'], lang='fr')
        tts.save('{}_fr.mp3'.format(word['id']))
        audio = '[sound:{}_fr.mp3]'.format(word['id'])
        new_note = genanki.Note(
          model=build_up_model,
          fields=[sentences[i]['fields']['Video ID'],
            sentences[i]['fields']['Line ID'],
            word['fields']['English (manual)'],
            word['fields']['French'],
            word['fields']['Sîplemê frâsé'],
            word['fields']['Phonetic'],
            word['fields']['TTS'],
            audio
            ]
        )
        video_deck.add_note(new_note)
        package.media_files.append('{}_fr.mp3'.format(word['id']))
    except KeyError:
      pass
    try:
      for phrase_id in sentences[i]['fields']['Key Phrases']:
        phrase = key_phrases.get(phrase_id)
        print(phrase['fields']['French'])
        tts = gTTS(phrase['fields']['TTS'], lang='fr')
        tts.save('{}_fr.mp3'.format(phrase['id']))
        audio = '[sound:{}_fr.mp3]'.format(phrase['id'])
        new_note = genanki.Note(
          model=build_up_model,
          fields=[sentences[i]['fields']['Video ID'],
            sentences[i]['fields']['Line ID'],
            phrase['fields']['English (manual)'],
            phrase['fields']['French'],
            phrase['fields']['Sunpleman Fransé'],
            phrase['fields']['Phonetic_ipa'],
            phrase['fields']['TTS'],
            audio
            ]
        )
        video_deck.add_note(new_note)
        package.media_files.append('{}_fr.mp3'.format(phrase['id']))
    except KeyError:
      pass
    print(sentences[i]['fields']['French'])
    starttime = srt_time_to_sec(sentences[i]['fields']['Time Start'])
    endtime = srt_time_to_sec(sentences[i]['fields']['Time Stop'])
    cut_name = 'Video_{}_Line_{}.mp4'.format(sentences[i]['fields']['Video ID'],sentences[i]['fields']['Line ID'])
    tag_cut_name = "[sound:{}]".format(cut_name)
    # generate the video file
    ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=cut_name) # -c:a aac
    sentence_note = genanki.Note(
    model=video_recognition,
    fields=[sentences[i]['fields']['Video ID'],
      sentences[i]['fields']['Line ID'],
      tag_cut_name,
      sentences[i]['fields']['French'],
      sentences[i]['fields']['English (manual)'],
      sentences[i]['fields']['IPA Pronunciation'],
      sentences[i]['fields']['Line sunpleman fransé']

      ]
    )
    video_deck.add_note(sentence_note)
    package.media_files.append(cut_name)
    print('added a sentence to video_deck')
#video_deck.add_note(new_note)
  package.write_to_file('video{}_deck.apkg'.format(str(selected_video)))

generate_anki_deck(video_id,video_name)
