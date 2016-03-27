import urllib2
import json
import calendar
import csv
import requests
import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def scrapetojson():
  file_name = 'posts.json'
  fout = open(file_name,'w')

  with open('../static/data/comments.txt', 'r') as data_file:
    data = json.load(data_file)

  #first step, organize comments by post and time

  #hash post id -> tuple (child comments in array, earliest time)
  posts = {}

  rows = data['data']

  for row in rows:
    if row['fromid'] not in posts:
      entry = ([row['text']], row['time'])  
      posts[row['fromid']]= entry
    else:
      entry = (posts[row['fromid']][0] + [row['text']] , posts[row['fromid']][1])
      if posts[row['fromid']][1] > row['time']:
        entry = (posts[row['fromid']][0] + [row['text']] , row['time'])
      posts[row['fromid']] = entry

  #second step, sentiment analysis on each post's replies
  post_json = analyze(posts)
  print post_json
  fout.write(json.dumps(post_json))

def setup_json():
  #Want to make json like this
  #'name': 'pos',
  #'children': [
    #more
    #'children': [
      #'name': ID, "size": compound_val
    #]
    #mid
    #less
  #]
  #neg
    #more
    #mid
    #less

  post_json = {}
  post_json['name'] = 'posts'
  post_json['children'] = []
  positive = {}
  neutral = {}
  negative = {}
  positive['name'] = 'positive'
  neutral['name'] = 'neutral'
  negative['name'] = 'negative'
  positive['children'] = []
  neutral['children'] = []
  negative['children'] = []

  min_pos = {}
  min_pos['name'] = 'min_pos'
  min_pos['children'] = []
  mid_pos = {}
  mid_pos['name'] = 'mid_pos'
  mid_pos['children'] = []
  max_pos = {}  
  max_pos['name'] = 'max_pos'
  max_pos['children'] = []
  min_neg = {}
  min_neg['name'] = 'min_neg'
  min_neg['children'] = []
  mid_neg = {}
  mid_neg['name'] = 'mid_neg'
  mid_neg['children'] = []
  max_neg = {}
  max_neg['name'] = 'max_neg'
  max_neg['children'] = []

  positive['children'].append(min_pos)
  positive['children'].append(mid_pos)
  positive['children'].append(max_pos)

  negative['children'].append(min_neg)
  negative['children'].append(mid_neg)
  negative['children'].append(max_neg)

  post_json['children'].append(positive)
  post_json['children'].append(neutral)
  post_json['children'].append(negative)

  print json.dumps(post_json)
  return post_json

def analyze(posts):
  post_json = setup_json()
  #for post, replies in posts.iteritems()

  sid = SentimentIntensityAnalyzer()
  for key, value in posts.iteritems():
    nustring = ' '.join(value[0]).replace("u'", "")
    ss = sid.polarity_scores(nustring)
    for k in sorted(ss):
      if k is "compound":
        entry = {}
        entry['name'] = ss[k]*len(nustring)
        entry['size'] = len(nustring)
        if ss[k] == 0.0:
          post_json['children'][1]['children'].append(entry)
        elif ss[k] < -0.8:
          post_json['children'][2]['children'][2]['children'].append(entry)
        elif ss[k] < -0.4:
          post_json['children'][2]['children'][1]['children'].append(entry)
        elif ss[k] < -0.0:
          post_json['children'][2]['children'][0]['children'].append(entry)
        elif ss[k] < 0.4:
          post_json['children'][0]['children'][0]['children'].append(entry)
        elif ss[k] < 0.8:
          post_json['children'][0]['children'][1]['children'].append(entry)
        else:
          post_json['children'][0]['children'][2]['children'].append(entry)
  return post_json


scrapetojson()
















