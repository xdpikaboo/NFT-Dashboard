from utils import logging
from crawling.crawler import Crawler
import db
from anal import Anal

class Processing:
    def __init__(self, sentiment_tokenizer, emotion_tokenizer, spam_tokenizer, model_sentiment, model_emotion, model_spam):
        self.sentiment_tokenizer = sentiment_tokenizer
        self.emotion_tokenizer = emotion_tokenizer
        self.spam_tokenizer = spam_tokenizer

        self.model_sentiment = model_sentiment
        self.model_emotion = model_emotion
        self.model_spam = model_spam
        self.anal = Anal(self.sentiment_tokenizer, self.emotion_tokenizer, self.spam_tokenizer, self.model_sentiment, self.model_emotion, self.model_spam)
        self.crawler = Crawler()
    def avg(self, lis):
        if len(lis) == 0:
            return 0
        return sum(lis) / len(lis)

    def add_tag(self, dict, tag):
        new_dict = {}
        for key in dict:
            new_dict[f'{tag}_{key}'] = dict[key]
        
        return new_dict

    def processing_collection_without_writing(self, collection):
        twitter_url = collection['twitter']
        crawl_result = self.crawler.crawl_twitter(twitter_url)
        twitter_data = self.processing_training_data(crawl_result)
    
        new_collection = {
            **collection,
            **self.add_tag(twitter_data, 'twitter')
        }
        return new_collection

    def processing_training_data(self, twitter_data):
        logging.info("PROCESSING DATA........")
        tweets_data = twitter_data['retweets_data']
        
        avg_likes = self.avg([data['public_metrics']['like_count'] for data in tweets_data])
        avg_reply = self.avg([data['public_metrics']['reply_count'] for data in tweets_data])
        avg_quote = self.avg([data['public_metrics']['quote_count'] for data in tweets_data])
        avg_retweet = self.avg([data['public_metrics']['retweet_count'] for data in tweets_data])

        retweets_data = twitter_data['retweets_data']
        
        tweets_text = {data['text']:{"id": data['id'], "created_at": data['created_at']} for data in retweets_data}

        analysis_metrics = self.anal.analyze_tweets(tweets_text, twitter_data['collection_data'])

        saved_data = {
            'avg_likes': avg_likes,
            'avg_reply': avg_reply,
            'avg_quote': avg_quote,
            'avg_retweet': avg_retweet,
            **analysis_metrics,
            **twitter_data['collection_data']['public_metrics']
        }

        print(saved_data)
        return saved_data

    def processing_collection(self, collection):
        db.write_metrics(self.processing_collection_without_writing(collection))
