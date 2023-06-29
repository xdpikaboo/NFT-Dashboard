import time
import json
from analysis.utils import logging
import requests
import re
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import pytz
from datetime import datetime, timedelta
from dateutil import parser

class Crawler():
    def __init__(self, max_tweets=50):
        self.MAX_TWEETS = max_tweets

        self.TOKEN_LIST = [
            'AAAAAAAAAAAAAAAAAAAAANmGQQEAAAAAU%2FFD1pctqU9d8QEnJuYegAWI7Gg%3DvxNAUmFtxxUPRpCtfPcl5j7FyBbqzRPNxoRxEhBCbdA6tIjqLv',
            'AAAAAAAAAAAAAAAAAAAAAF9lZQEAAAAAfJi0sna3YwoxlZ0WW84HdyY74BA%3DGbwIxBQz83eChkdNcqOSiCcHDncxpWpMAGJyK2gPVDsMnL8oIt',   
            'AAAAAAAAAAAAAAAAAAAAAARDZgEAAAAADYYkyRrrYyhAYVuNpBY%2Bguqu5D8%3DlRKskVNz9fd9FvWaLGpJVonzzscugcD5l5FGLaLT9NWx6zaO82', 
            'AAAAAAAAAAAAAAAAAAAAAMlmZAEAAAAAJ%2Bizx52ZQp4GuNPBn2Q5ZHVYUaI%3D88pFf4rm7aID4yjYj7Bpk7lFG5pTVW2Fsmh4IlFnUKhA3TP3Ki', 
            'AAAAAAAAAAAAAAAAAAAAACii6QAAAAAAcm9MSth7nqAXO80q6j6rtmHVu5Q%3D5dLyPGVkTm1lu8bhjWOXM1RLe0wSnXhjiWgDkT4yn8urLta9Uq', 
            'AAAAAAAAAAAAAAAAAAAAADshcAEAAAAAKphEqM9INoFMpcQUYpjmElRaSxc%3D4cEXtxAHIhrLNaFQLmPtiZYwUNi1ZHYytnST76xABdq23XGD3e', 
            'AAAAAAAAAAAAAAAAAAAAAFEgcAEAAAAAvUL2ZU6Z9WUMHU1H31iAR%2BNJXLc%3DXAwgE5rjUWtkACtbPtyad4Q82FenYxvN7HgHooSFfIWHVHdP1Q', 
            'AAAAAAAAAAAAAAAAAAAAAOAhcAEAAAAA6TR5xLM3%2FB5yEKy8NM8sLMYZ1l8%3Dtp35xnDx8WCD0jHT44BEXqfu3ywkzg8i6CSqxvwNaAKh9owmqs', 
            'AAAAAAAAAAAAAAAAAAAAAClAbAEAAAAAtXO8Co4bSkmGmWUx77ZPjYQneqM%3DaIPAHGm6SBw9MJpYnVG8Zfgv7sb7L6AHlt3SNX4bqpODd4rLTR', 
            'AAAAAAAAAAAAAAAAAAAAAL%2F9cgEAAAAASPq0PwHy7ODA1ksg95iWISa7znE%3Dgbi4HPTwySmsjLujfD98YFWbwiVOu8PRKZOU5SI4hbmgRZQtAx', 
            'AAAAAAAAAAAAAAAAAAAAAOz9cgEAAAAA8g54SXVnUx6kktUQ239xmtLZE%2Bs%3D7B47SFaHZr4yTaA0gzM7ks50W08KlEPaTDeqBSQoMgMQ9cmec0', 
            'AAAAAAAAAAAAAAAAAAAAAAn%2BcgEAAAAAUFth6iYg3CpSmyul9CiXdUYage8%3D48qI0VLiwguasX4UVKrqwZvIMLqwQt5PKJwykeKYYb2W2PTFdp', 
            'AAAAAAAAAAAAAAAAAAAAADr%2BcgEAAAAASKIajwVBfHJEGgI2aBKwUpE2WnY%3DOyMKbUHgen9Uodq5AqxBGOoD1XXhtQo8bH2cPEuXG5fVbCRABw', 
            'AAAAAAAAAAAAAAAAAAAAAHD%2BcgEAAAAA%2Bk%2F3Hx%2BEqAZF9gtRPHz1Uf7UZQA%3DGvCP2VLnbpPNT38fIK6zc51neV5KkxeeSIrzpfSc0iFnUSy0vw', 
            'AAAAAAAAAAAAAAAAAAAAAKP%2BcgEAAAAAME%2FkNOtZwk92G7Yd3YTCaMEMNRw%3DeNsqKEIpzSnJpa5nnSAUHxaA5aed4Su57w2ihGK3OyJlrGLjW8', 
            'AAAAAAAAAAAAAAAAAAAAALr%2BcgEAAAAA702rhkJ2k5tM97UsP8gNnR6u0W0%3D5nC1sbBqIDaWuZIXjOGdnlmrGL4JeCAdkjcLHrf9SSuSC6ncuw',
            'AAAAAAAAAAAAAAAAAAAAAKtqcwEAAAAA5bzWcvLrRlMlTzjX7C7h1p3R7Ms%3DgZ622s5XMmzhKB2qWWy0tTk0j7i76W9ogRhk5FXIj5wXGgM7L2',
            'AAAAAAAAAAAAAAAAAAAAAMZqcwEAAAAAgONybl%2FEje7mgLzbVl1LeL8L19I%3D7zkf8gGdt1MG0EnujYOgOYyCrqEWyaK5Kt65vn6D10kPjtANbj', 
        ]
        self.token_idx = 0
        
    def crawl_url(self, url):
        try:
            userAgent = UserAgent().random

            options = webdriver.ChromeOptions()
            options.add_argument('-headless')
            options.add_argument('-no-sandbox')
            options.add_argument('-disable-dev-shm-usage')
            options.add_argument(f'user-agent={userAgent}')
            options.add_argument("--incognito")
            options.add_argument('start-maximized')
            
            wd = webdriver.Chrome('chromedriver' ,options=options)
            wd.get(url)
            # html = wd.find_element_by_xpath("//body").get_attribute('outerHTML')
            json_obj = json.loads(wd.find_element(By.TAG_NAME, 'pre').text)
            return json_obj
        except Exception as e:
            logging.error(f"Magic Eden server does not respond! {e}")
            return []
    
    def crawl_me_one_tag(self, tag):
        try:
            if tag != "new_collections":
                url =  f'''https://stats-mainnet.magiceden.io/collection_stats/popular_collections/sol?window={tag}&limit=30'''
            else:
                url = f'''https://api-mainnet.magiceden.io/{tag}?more=true'''
            res = self.crawl_url(url)
            new_res = []
            for collection in res:
                if 'twitter' not in collection:
                    new_res.append(self.crawl_me_api_for_twitter(collection['collectionSymbol']))
            # print(new_res)
                        # 'tags': col['tags']
            return new_res
        except Exception as e:
            logging.error(f"No response {e} for {tag}")
            return []

    def crawl_collection_overall_stats(self, name):
        try:
            url = f'''https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{name}'''
            json_obj = self.crawl_url(url)
            return json_obj['results'] if 'results' in json_obj else None
        except Exception as e:
            logging.error("No response {e}")
            return []

    def crawl_volume_24h(self, obj):
        return obj['volume24hr'] if 'volume24hr' in obj and obj['volume24hr'] != None else -1

    def crawl_volume_all(self, obj):
        return obj['volumeAll'] if 'volumeAll' in obj and obj['volumeAll'] != None else -1

    def crawl_floor_price(self, obj):
        return obj['floorPrice'] if 'floorPrice' in obj and obj['floorPrice'] != None else -1

    def crawl_total_listing(self, obj):
        return obj['listedCount'] if 'listedCount' in obj and obj['listedCount'] != None else -1

    def crawl_collection_info(self, name):
        try:
            url = f'https://api-mainnet.magiceden.io/collections/{name}?edge_cache=true'
            json_obj = self.crawl_url(url)
            return json_obj if 'symbol' in json_obj else None
        except Exception as e:
            logging.error("No response {e}")
            return []

    def api_call(self, endpoint, headers, params):
        MAX_TIME = 150
        current_time = 1
        while True:
            try:
                response = requests.get(endpoint, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    return data
                elif response.status_code == 429 or response.status_code == 401:
                    if self.token_idx == len(self.TOKEN_LIST) - 1:
                        self.token_idx = 0
                    else:
                        self.token_idx = self.token_idx + 1
                    return None
                else:
                    raise ValueError(response)

            except Exception as e:
                logging.error(f'Error found: {e}, {endpoint}')
                if current_time >= MAX_TIME:
                    raise ValueError(f"""
                    Cannot get data from {endpoint}
                    Headers: {headers}
                    Params: {params}
                    """)
                logging.info(f'Retry after {current_time}s.')
                time.sleep(current_time)
                current_time *= 2

    def crawl_me_api_for_twitter(self, symbol):
        url = f"https://api-mainnet.magiceden.io/collections/{symbol}"
        return self.crawl_url(url)

    def crawl_twitter(self, url):
        start = time.time()
        pattern =  '^https?:\/\/(?:www\.)?twitter\.com\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?$'
        url = url.strip()
        username = re.match(pattern, url).group(1)

        username_endpoint = f'https://api.twitter.com/2/users/by/username/{username}'
        
        TOKEN = self.TOKEN_LIST[self.token_idx]
        
        headers = {"Authorization": f"Bearer {TOKEN}"}
        

        logging.info(f'Collection name: {username}')

        user_params = {
            'user.fields': 'public_metrics,description'
        }

        api_call_res = self.api_call(endpoint=username_endpoint, headers=headers, params=user_params)
        
        user_data = api_call_res['data']
        user_id = user_data['id']

        # timeline_endpoint = f'https://api.twitter.com/2/users/{user_id}/tweets'
        search_endpoint = f'https://api.twitter.com/2/tweets/search/recent'
        
        retweets_data = []
        pagination_token = None

        while True:

            retweets_params = {
                'query' : f'@{username}',
                'tweet.fields' : 'public_metrics,created_at'
            }
            if pagination_token:
                retweets_params['pagination_token'] = pagination_token
            

            response_data = self.api_call(search_endpoint, headers = headers, params=retweets_params)
            if response_data == None:
                TOKEN = self.TOKEN_LIST[self.token_idx]
                headers = {"Authorization": f"Bearer {TOKEN}"}
                continue

            retweet_split_data = response_data.get('data', [])
            meta_data = response_data['meta']
            

            retweets_data = retweets_data + retweet_split_data

            
            if 'next_token' in meta_data and len(retweets_data) < self.MAX_TWEETS:
                pagination_token = meta_data['next_token']
            else:
                break
        end = time.time()
        logging.info(f'Finished {username} retweets in {end - start}!')
        
        return {
            'collection_data': user_data,
            # 'tweets_data': tweets_data,
            'retweets_data': retweets_data,
        }

    def after_today(self, s):
        utc=pytz.UTC
        date = parser.parse(s)
        cur_date = datetime.utcnow()
        cur_date = utc.localize(cur_date)
        return date >= cur_date
    
    def within_7days(self, s):
        utc=pytz.UTC
        date = parser.parse(s)
        cur_date = datetime.utcnow()
        cur_date = utc.localize(cur_date)
        seven_days_after = cur_date + timedelta(weeks=1)
        return date <= seven_days_after

    def get_all_me_collections_by_tags(self, tags):
        res_map = {}
        for tag in tags:
            res = self.crawl_me_one_tag(tag)
            res_map[tag] = res
        return res_map
    
    def convert_upcoming_to_db_format(self, obj):
        img = obj['assets']['profileImage']
        link = obj['links']
        obj.pop('links')
        obj.pop('assets')
        obj = {
            **obj,
            **link,
            'image': img
        }
        return obj


    def get_top_upcoming_collection(self, limit=20, sort_by='upvote'):
        url = 'https://api-mainnet.magiceden.io/drops?limit=250&offset=0'
        res = self.crawl_url(url)
        json_data = list(filter(lambda x: self.after_today(x['launchDate']), res))
        json_data = list(filter(lambda x: self.within_7days(x['launchDate']), json_data))
        json_data.sort(key=lambda x: -int(x[sort_by]))
        json_data = json_data[:limit]
        json_data = list(map(self.convert_upcoming_to_db_format, json_data))
        result = {'me-upcoming': json_data}
        return result
