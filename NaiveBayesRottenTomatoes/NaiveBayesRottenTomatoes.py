# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 14:56:43 2021

@author: georg
"""

import pandas as pd
import numpy as np
import nltk, keras, string, re, html, math

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter, defaultdict
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import accuracy_score, classification_report

#set seed
#nltk.download()
np.random.seed(25)
rottenTomatoes=pd.read_csv('C:/Users/georg/Desktop/rotten_tomatoes_reviews_sample.csv', index_col=False)

## data cleaning and feature creation
def cleaning(data):
    clean = re.sub('<.*?>', ' ', str(data))                         
#removes all hanging letters afer apostrophes (s in it's)
    clean = clean.translate(str.maketrans('', '', string.punctuation))                          
#replacing the non alphanumeric characters
    return html.unescape(clean.lower())
rottenTomatoes['cleaned'] = rottenTomatoes['Review'].apply(cleaning)

#create token for phrases
def tokenizing(data):
    review = data['cleaned']                            
#tokenizing is done
    tokens = nltk.word_tokenize(review)
    return tokens
rottenTomatoes['tokens'] = rottenTomatoes.apply(tokenizing, axis=1)

#remove stopwords 
stop_words = set(stopwords.words('english'))
def remove_stops(data):
    my_list = data['tokens']
    meaningful_words = [w for w in my_list if not w in stop_words]           #stopwords are removed from the tokenized data
    return (meaningful_words)
rottenTomatoes['tokens'] = rottenTomatoes.apply(remove_stops, axis=1)

#lemmatizing is performed.
lemmatizer = WordNetLemmatizer()
def lemmatizing(data):
    my_list = data['tokens']
    lemmatized_list = [lemmatizer.lemmatize(word) for word in my_list]    
    return (lemmatized_list)
rottenTomatoes['tokens'] = rottenTomatoes.apply(lemmatizing, axis=1)

## data exploration and summarization 

# Prints statistics of Data like avg length of sentence , proportion of data w.r.t class labels
def sents(data):
    clean = re.sub('<.*?>', ' ', str(data))            
#removes HTML tags
    clean = re.sub('\'.*?\s',' ', clean)               
#removes all hanging letters afer apostrophes (s in it's)
    clean = re.sub(r'http\S+',' ', clean)              
#removes URLs
    clean = re.sub('[^a-zA-Z0-9\.]+',' ', clean)       
#removes all non-alphanumeric characters except periods.
    tokens = nltk.sent_tokenize(clean)                 
#sentence tokenizing is done
    return tokens
sents = rottenTomatoes['Review'].apply(sents)

length_s = 0
for i in range(rottenTomatoes.shape[0]):
    length_s+= len(sents[i])
print("The number of sentences is - ", length_s)          
#prints the number of sentences

length_t = 0
for i in range(rottenTomatoes.shape[0]):
    length_t+= len(rottenTomatoes['tokens'][i])
print("\nThe number of tokens is - ", length_t)           
#prints the number of tokens

average_tokens = round(length_t/length_s)
print("\nThe average number of tokens per sentence is - ", average_tokens) 
#prints the average number of tokens per sentence

fresh = rotten = 0
for i in range(rottenTomatoes.shape[0]):
    if (rottenTomatoes['Freshness'][i]=='fresh'):
        fresh += 1                           
#finds the proprtion of positive and negative sentiments
    else:
        rotten += 1

print("\nThe number of fresh examples are - ", fresh)
print("\nThe number of rotten examples are - ", rotten)
print("\nThe proportion of positive to negative sentiments are -", fresh/rotten)

## encode variables 
# gets reviews column from df
reviews = rottenTomatoes['cleaned'].values

# gets labels column from df
labels = rottenTomatoes['Freshness'].values
# Uses label encoder to encode labels. Convert to 0/1
encoder = LabelEncoder()
encoded_labels = encoder.fit_transform(labels)
rottenTomatoes['encoded']= encoded_labels

# prints(enc.classes_)
encoder_mapping = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))

# Splits the data into train and test (80% - 20%). 
# Uses stratify in train_test_split so that both train and test have similar ratio of positive and negative samples.
train_sentences, test_sentences, train_labels, test_labels = train_test_split(reviews, labels, test_size=0.2, random_state=42, stratify=labels)

# Uses Count vectorizer to get frequency of the words
vectorizer = CountVectorizer(max_features = 8000)

sents_encoded = vectorizer.fit_transform(train_sentences)#encodes all training sentences
counts = sents_encoded.sum(axis=0).A1
vocab = list(vectorizer.get_feature_names())

# Uses laplace smoothing for words in test set not present in vocab of train set.
def laplace_smoothing(self, word, text_class):
  num = self.word_counts[text_class][word] + 1
  denom = self.n_class_items[text_class] + len(self.vocab)
  return math.log(num / denom)

class MultinomialNaiveBayes:
  
    def __init__(self, classes, tokenizer):
      self.tokenizer = tokenizer
      self.classes = classes
      
    def group_by_class(self, X, y):
      data = dict()
      for c in self.classes:                            
#grouping by positive and negative sentiments
        data[c] = X[np.where(y == c)]
      return data
           
    def fit(self, X, y):
        self.n_class_items = {}
        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = vocab                            
#using the pre-made vocabulary of n most frequent training words

        n = len(X)
        
        grouped_data = self.group_by_class(X, y)
        
        for c, data in grouped_data.items():
          self.n_class_items[c] = len(data)
          self.log_class_priors[c]=math.log(self.n_class_items[c]/n)
#taking log for easier calculation
          self.word_counts[c] = defaultdict(lambda: 0)
          
          for text in data:
            counts = Counter(nltk.word_tokenize(text))
            for word, count in counts.items():
                self.word_counts[c][word] += count
                
        return self
    def laplace_smoothing(self, word, text_class):          #smoothing
      num = self.word_counts[text_class][word] + 1
      denom = self.n_class_items[text_class] + len(self.vocab)
      return math.log(num / denom)
      
    def predict(self, X):
        result = []
        for text in X:
          
          class_scores = {c: self.log_class_priors[c] for c in self.classes}

          words = set(nltk.word_tokenize(text))
          for word in words:
              if word not in self.vocab: continue

              for c in self.classes:
                
                log_w_given_c = self.laplace_smoothing(word, c)
                class_scores[c] += log_w_given_c
                
          result.append(max(class_scores, key=class_scores.get))

        return result
    
MNB = MultinomialNaiveBayes(
    classes=np.unique(labels), 
    tokenizer=Tokenizer()
).fit(train_sentences, train_labels)

# Tests the model on test set and reports the Accuracy
predicted_labels = MNB.predict(test_sentences)
print("The accuracy of the MNB classifier is ", accuracy_score(test_labels, predicted_labels))
print("\nThe classification report with metrics - \n", classification_report(test_labels, predicted_labels))   