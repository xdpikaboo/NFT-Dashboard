import db
from datetime import datetime, timedelta
from pytz import timezone
from utils import logging

class MetricShock:
    def __init__(self, name, last):
        self.last = last
        self.name = name

    def get_all_metric_shock(self):
        shock1hr = self.all_metric_change_for_one_collection_by_period(1)
        shock6hr = self.all_metric_change_for_one_collection_by_period(6)
        shock1d = self.all_metric_change_for_one_collection_by_period(24)
        shock3d = self.all_metric_change_for_one_collection_by_period(24 * 3)
        shock7d = self.all_metric_change_for_one_collection_by_period(24 * 7)
        return {
            "shock1hr": shock1hr,
            "shock6hr": shock6hr,
            "shock1d": shock1d,
            "shock3d": shock3d,
            "shock7d": shock7d
        }

    def one_metric_change(self, metric, first, last):
        firstPt = -1
        lastPt = -1 
        if metric in first: 
            firstPt = first[metric]
        if metric in last:
            lastPt = last[metric]
        if firstPt < 0 or lastPt < 0:
            return None
        return (lastPt - firstPt) / firstPt * 100

    def query_first(self, period):
        try:
            date = datetime.now()
            compare_date = (date - timedelta(hours = period)).strftime("%Y-%m-%d %H:%M:%S")
            
            compare_date = {"$dateFromString": { 
                                    "dateString": compare_date,
                                    "format": "%Y-%m-%d %H:%M:%S",
                                    "timezone": "UTC" 
                                }
                            }
            db_date = {"$dateFromString": { 
                                    "dateString": "$createdAt",
                                    "format": "%Y-%m-%d %H:%M:%S",
                                    "timezone": "America/New_York" 
                                }
                            }

            query = {'name': self.name,
                        "$expr" : { 
                            "$gte": [db_date, compare_date]
                        }
                    }
            
            time_series_col = db.get_collection('time_series')
            
            result = list(time_series_col.find(query).limit(1))
            return result
        except Exception as e:
            logging.error(f"In metric_change bugs {e} for {self.name}")
            return []
    
    def all_metric_change_for_one_collection_by_period(self, period):
        try:
            result = self.query_first(period)
            if result == []:
                return None
            firstPt = result[0]
            lastPt = self.last
            
            volume24h = self.one_metric_change('volume24h', firstPt, lastPt)
            listedCount = self.one_metric_change('listedCount', firstPt, lastPt)
            floorPrice = self.one_metric_change('floorPrice', firstPt, lastPt)
            volumeAll = self.one_metric_change('volumeAll', firstPt, lastPt)
            followers_count = self.one_metric_change('twitter_followers_count', firstPt, lastPt)
            following_count = self.one_metric_change('twitter_following_count', firstPt, lastPt)
            tweet_count = self.one_metric_change('twitter_tweet_count', firstPt, lastPt)
            sentiment = self.one_metric_change('twitter_sent_avg_norm', firstPt, lastPt)

            return {
                    "volume": volume24h,
                    "listedCount": listedCount,
                    "floorPrice": floorPrice,
                    "volumeAll": volumeAll,
                    "followers_count": followers_count,
                    "following_count": following_count,
                    "tweet_count": tweet_count,
                    "sentiment": sentiment
                    }
        except Exception as e:
            logging.info(f'In metric_change {self.name} has {e}')
            return None
    
    def query_last(self, period):
        try:
            date = datetime.now()
            compare_date = (date - timedelta(hours = period)).strftime("%Y-%m-%d %H:%M:%S")
            
            compare_date = {"$dateFromString": { 
                                    "dateString": compare_date,
                                    "format": "%Y-%m-%d %H:%M:%S",
                                    "timezone": "UTC" 
                                }
                            }
            db_date = {"$dateFromString": { 
                                    "dateString": "$createdAt",
                                    "format": "%Y-%m-%d %H:%M:%S",
                                    "timezone": "America/New_York" 
                                }
                            }

            query = {'name': self.name,
                        "$expr" : { 
                            "$gte": [db_date, compare_date]
                        }
                    }
            
            time_series_col = db.get_collection('time_series')
            
            result = list(time_series_col.find(query))
            return result
        except Exception as e:
            logging.error(f"In metric_change bugs {e} for {self.name}")
            return []