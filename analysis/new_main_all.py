from utils import logging
import db
from crawling.crawler import Crawler
import time
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import pprint

tag_map = {
            '1h': 'popular-collections-1h', 
            '1d': 'popular-collections-1day', 
            '7d': 'popular-collections-7days', 
            '30d': 'popular-collections-30days'
            }

tags = [
'1h', 
'1d', 
'7d', 
'30d'
]
pp = pprint.PrettyPrinter()
def process_all_collections_for_db(tag_to_data):
    symbol_map = {}
    for tag, data in tag_to_data.items():
        for col in data:
            if 'symbol' not in col:
              continue
            symbol = col['symbol']
            if symbol not in symbol_map:
                symbol_map[symbol] = {
                    **col,
                    **{v: False for k, v in tag_map.items()}
                }

    for tag, data in tag_to_data.items():
        for col in data:
            if 'symbol' not in col:
              continue
            symbol = col['symbol']
            db_tag = tag_map[tag]
            symbol_map[symbol][db_tag] = True

    return list(symbol_map.values())

def map_nfts_to_tag(all_nfts_stat, tags):
  nft_map = {tag: [] for tag in tags}
  for nft in all_nfts_stat:
    for tag in nft_map.keys():
      if nft[tag] == True:
        if '_id' in nft:
          nft.pop('_id')
        nft_map[tag].append({
                              **nft,
                              'tag': tag
                            })
  return nft_map

if __name__ == '__main__':
    while True:
      start = time.time()
      logging.info("Start the sentiment LOOP!")
      data_cols = []
      
      SENTIMENT = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
      EMOTION = 'cardiffnlp/twitter-roberta-base-emotion'
      SPAM = "mrm8488/bert-tiny-finetuned-sms-spam-detection"

      sentiment_tokenizer = AutoTokenizer.from_pretrained(SENTIMENT)
      emotion_tokenizer = AutoTokenizer.from_pretrained(EMOTION)
      spam_tokenizer = AutoTokenizer.from_pretrained(SPAM)

      model_sentiment = AutoModelForSequenceClassification.from_pretrained(SENTIMENT)
      model_emotion = AutoModelForSequenceClassification.from_pretrained(EMOTION)
      model_spam = AutoModelForSequenceClassification.from_pretrained(SPAM)
      ### Getting collections from Sol database

      import get_collections
      collection_analysis = get_collections.Get_Collection(sentiment_tokenizer,
                                            emotion_tokenizer,
                                            spam_tokenizer,
                                            model_sentiment,
                                            model_emotion,
                                            model_spam,
                                            50)
      crawler = Crawler()
      
      all_me_collections_by_tags = crawler.get_all_me_collections_by_tags(tags)
      
      all_collections = {
        **all_me_collections_by_tags,
      }

      all_cols_for_db = process_all_collections_for_db(all_collections)
      db.drop_all_then_insert_many(all_cols_for_db, 'all_nfts')
      
      all_nfts_stat = collection_analysis.get_all_collections(all_cols_for_db)
      
      db_tag = list(tag_map.values())
      nfts_by_tag = map_nfts_to_tag(all_nfts_stat, db_tag)
      for tag, nfts in nfts_by_tag.items():
        data_cols_by_tag = nfts_by_tag[tag]
        db.drop_then_insert(data_cols_by_tag, tag)

      logging.info("Finish the sentiment LOOP!")
      logging.info(f'TOTAL TIME {(time.time() - start) / 60}')
      logging.info("WAITTTTT")
    
      # print(f'Sleep for 10 minutes')
      time_sleep = 5
      logging.info(f'Sleep for {time_sleep} minutes')
      # print(f'Sleep for 10 minutes')
      time.sleep(time_sleep * 60)

