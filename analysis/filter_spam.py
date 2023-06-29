import time
import datasets
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
import torch
from itertools import compress

MAX_LENGTH = 256
BATCH_SIZE = 16

def map_boolean(num):
  return True if num == 0 else False

def filter_spam(tweets_dict, tokenizer, model):
  tweets_list = tweets_dict['tweets']
  tweet_label = list(get_spam_tweet(tweets_dict, tokenizer, model))

  spam_tweets_boolean = list(map(bool, tweet_label))

  tweets_boolean = list(map(map_boolean, tweet_label))

  non_spam_tweets = list(compress(tweets_list, tweets_boolean))

  return non_spam_tweets

def get_spam_tweet(tweets_list, tokenizer, model):
    model = model.to("cuda")
    
    return predict_spam_tweet(tokenizer, tweets_list, model)


def preprocess(text):
    new_text = []

    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = '@http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def preprocess_tweets(tweets):
  return tweets

def convert_tweets_for_training(tokenizer, tweets):
  clean_tweets = preprocess_tweets(tweets)
  encoded_input = tokenizer(clean_tweets, return_tensors='pt', padding="max_length", truncation=True, max_length=MAX_LENGTH)
  return encoded_input

def generate_softmax_score(batch, model):
  input_ids = torch.tensor(batch['input_ids']).to("cuda")
  attention_mask = torch.tensor(batch['attention_mask']).to("cuda")
  output = model(input_ids=input_ids, attention_mask=attention_mask)
  
  softmax_layer = torch.nn.Softmax()
  scores = softmax_layer(output[0]).cpu()
  scores = scores.detach().numpy()
  pred = [np.argmax(score) for score in scores]
  batch['pred'] = pred
  return batch

def predict_spam_tweet(tokenizer, collection, model):
  tweets = collection['tweets']
  if not tweets:
    return f"{collection['name']} has empty list of tweets"
  processed_tweets = convert_tweets_for_training(tokenizer, tweets)

  dataset_tweets = datasets.Dataset.from_dict(processed_tweets)
  result = dataset_tweets.map(lambda batch: generate_softmax_score(batch, model), batched=True, batch_size=BATCH_SIZE)
  pred = result['pred']

  return pred
  