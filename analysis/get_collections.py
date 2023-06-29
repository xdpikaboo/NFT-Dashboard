import time
from processing import Processing
import db
from datetime import datetime
from pytz import timezone
from crawling.crawler import Crawler
from utils import logging
from metric_shock import MetricShock

ONE_BIL = 1000000000
class Get_Collection:
    def __init__(self, sentiment_tokenizer, emotion_tokenizer, spam_tokenizer, model_sentiment, model_emotion, model_spam, max_tweets):
        self.sentiment_tokenizer = sentiment_tokenizer
        self.emotion_tokenizer = emotion_tokenizer
        self.spam_tokenizer = spam_tokenizer

        self.model_sentiment = model_sentiment
        self.model_emotion = model_emotion
        self.model_spam = model_spam
        
        self.crawler = Crawler(max_tweets=max_tweets)
        self.processing = Processing(sentiment_tokenizer, emotion_tokenizer, spam_tokenizer, model_sentiment, model_emotion, model_spam)

    def analysis_on_collections(self, cols):
        data_cols = []

        for col in cols:
            result = self.analysis_on_one_collection(col)
            if result != None:
                data_cols.append(result)
        return data_cols

    def analysis_on_one_collection(self, col):
        start = time.time()
        result = None
        try:
            stats = self.processing.processing_collection_without_writing(col)
            #Last point of the shock period
            last_point = self.time_series_analysis(stats)
            metric_shock = MetricShock(stats['name'], last_point)
            #Calculate all metric shock
            shock = metric_shock.get_all_metric_shock()
            result = {
                **last_point,
                "shock": shock
            }
        except Exception as e:
            symbol = col['collectionSymbol']
            logging.error(f'Error durring handling collections {symbol}: {e}')
        finally:
            end = time.time()
            logging.info(f'Analysis time for {col["symbol"]} is {end - start}')
            return result        

    def time_series_analysis(self, result):
        logging.info("TIME SERIES...")
        fmt = "%Y-%m-%d %H:%M:%S"
        now_time = datetime.now(timezone('US/Eastern'))
        createdAt = now_time.strftime(fmt)
        floorPrice = -1
        volume24h = -1
        volumeAll = -1
        listedCount = -1
        symbol = result['symbol']
        collection_name = result['name']

        obj = self.crawler.crawl_collection_overall_stats(symbol)
        if 'tag' not in result or (result['tag'] != 'upcoming' and obj != None):
            floorPrice = self.crawler.crawl_floor_price(obj)
            volume24h = self.crawler.crawl_volume_24h(obj)
            volumeAll = self.crawler.crawl_volume_all(obj)
            listedCount = self.crawler.crawl_total_listing(obj)

        floorPrice = (floorPrice / ONE_BIL) if floorPrice > 0 else floorPrice
        volume24h = (volume24h / ONE_BIL) if volume24h > 0 else volume24h
        volumeAll = (volumeAll / ONE_BIL) if volumeAll > 0 else volumeAll

        instant = {
            **result,
            'createdAt': createdAt,
            'floorPrice': floorPrice,
            'volume24h': volume24h,
            'volumeAll': volumeAll,
            'listedCount': listedCount,
        }

        if '_id' in instant: del instant['_id']
        try:
            db.get_collection('time_series').insert_one(instant)
        except Exception as e:
            logging.error(f"{e} in time_series_analysis")

        return instant


    def get_all_collections(self, cols):
        start = time.time()

        logging.info(f'Start analysis on all magic eden items!')

        data_cols = self.analysis_on_collections(cols)
        
        end = time.time()
        
        logging.info(f'Total runtime for {len(cols)} collections from magic eden: {end - start} total')
            
        logging.info(f'Finish analysis on magic eden items!')

        return data_cols

    def get_collections_from_db(self, tag=None):
        ### Make this less-error prone, in case the database crashed or smth
        cur_wait_time = 1
        MAX_WAIT_TIME = 60
        while True:
            try:
                cols = db.get_db_rows(tag)
                break
            except Exception as e:
                logging.error(f'Error: try to access db again after {cur_wait_time}s because of {e}')
                if cur_wait_time > MAX_WAIT_TIME:
                    raise RuntimeError('Unknown error from database appear!')
                time.sleep(cur_wait_time)
                cur_wait_time *= 2

        start = time.time()

        logging.info(f'Start analysis on {tag} items!')

        data_cols = self.analysis_on_collections(cols)
        
        end = time.time()
        
        logging.info(f'Total runtime for {len(cols)} collections from {tag}: {end - start} total')
            
        logging.info(f'Finish analysis on {tag}!')

        return data_cols
