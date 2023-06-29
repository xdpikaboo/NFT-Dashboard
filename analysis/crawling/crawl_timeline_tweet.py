import requests
import json
import time 
import re
import pytz
from datetime import datetime

TOKEN_LIST = [
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

idx = len(TOKEN_LIST) - 1

token = TOKEN_LIST[idx]

def get_twitter_username(url):
    pattern =  '^https?:\/\/(?:www\.)?twitter\.com\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?$'
    url = url.strip()
    username = re.match(pattern, url).group(1)
    return username

def bearer_oauth(r, token):
  """
  Method required by bearer token authentication.
  """
  r.headers["Authorization"] = f"Bearer {token}"
  r.headers["User-Agent"] = "v2RecentSearchPython"
  return r

def get_twitter_response(url, auth, params, token):
  return json.loads(requests.get(url=url, auth=lambda r : auth(r, token), params=params).text)

def get_next_token(json_response):
  next_token = ''
  if 'meta' in json_response and 'next_token' in json_response['meta']:
      next_token = json_response['meta']['next_token']
  return next_token

def get_user_by_username(username):
  url = f'https://api.twitter.com/2/users/by/username/{username}'
  params = {
      "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
      "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,public_metrics,organic_metrics,promoted_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld"
  }
  found = False
  local_idx = 0
  local_token = TOKEN_LIST[local_idx]
  limit_token = set()
  while found == False:
    res = get_twitter_response(url, bearer_oauth, params, local_token)
    if 'data' not in res and 'status' in res:
      limit_token.add(local_token)
      local_idx = (local_idx + 1) % len(TOKEN_LIST)
      local_token = TOKEN_LIST[local_idx]
      if len(limit_token) == len(TOKEN_LIST):
        limit_token = set()
        local_idx = 0
        print("All tokens have been used. Sleep for 15 minutes! in get_user_by_username")
        print(res)
        time.sleep(15 * 60)
      continue
    else:
        found = True
        return res       
  
  return None

def get_user_id_by_username(username):
  user_info = get_user_by_username(username)
  try:
    return user_info['data']['id'] if user_info != None else None
  except:
    print(user_info)

def get_user_by_user_id(user_id):
  params = {
      "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
      "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,public_metrics,organic_metrics,promoted_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld"
  }
  url = f'https://api.twitter.com/2/users/{user_id}'
  return json.loads(requests.get(url=url, auth=bearer_oauth, params=params).text)

def get_iso_time(timestamp):
    tz = pytz.utc
    iso_time = datetime.fromtimestamp(timestamp, tz).isoformat()
    return iso_time

def get_all_timeline_tweets_by_username(username):
  user_id = get_user_id_by_username(username)
  if user_id == None: return []
  params = {
    'max_results': 100,
    'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld',
    'tweet.fields': 'author_id,conversation_id,created_at,in_reply_to_user_id,public_metrics,referenced_tweets,source,text',
    'start_time': '2010-11-06T00:00:00Z',
    'end_time': get_iso_time(time.time() - (24 * 60 * 10)).split(".")[0] + "Z"
  }
  url = f'https://api.twitter.com/2/users/{user_id}/tweets'
  all_followers = []

  pagination_token = ''
  has_next_page = True

  local_idx = 0
  local_token = TOKEN_LIST[local_idx]
  limit_token = set()
  while has_next_page:
    followers_res = get_twitter_response(url, bearer_oauth, params, local_token)
    data = []
    if 'data' not in followers_res and 'meta' not in followers_res:
      limit_token.add(local_token)
      local_idx = (local_idx + 1) % len(TOKEN_LIST)
      local_token = TOKEN_LIST[local_idx]
      if len(limit_token) == len(TOKEN_LIST):
        limit_token = set()
        local_idx = 0
        print("All tokens have been used. Sleep for 15 minutes! in get_tweets_by_username")
        time.sleep(15 * 60)
      continue
    elif 'data' in followers_res:
        data = followers_res['data']
    all_followers += data
    pagination_token = get_next_token(followers_res)
    if pagination_token:
      params['pagination_token'] = pagination_token
    else:
      has_next_page = False
  return all_followers

if __name__ == "__main__":      
    all_nfts_db = db.get_collection('all_nfts')
    all_nfts = all_nfts_db.find({})
    timeline_tweet_db = db.get_collection('timeline_tweets')
    twitters = set()
    for nft_json in all_nfts:
        twitter = nft_json['twitter']
        if twitter != '' and list(timeline_tweet_db.find({'twitter': twitter})) != []: continue
        twitters.add(twitter)
    print("Start crawling timeline tweets!")
    for twitter_url in twitters:
        try:
            username = get_twitter_username(twitter_url)
        
            print(f"Searching timeline tweets for {username}")
            timeline_tweets = get_all_timeline_tweets_by_username(username)
            
            if timeline_tweets == []: continue

            timeline_tweets_for_insert = [{'_id': tweet['id'], 
                                            'username': username, 
                                            'twitter': twitter_url, 
                                            **tweet} for tweet in timeline_tweets]
            timeline_tweet_db.insert_many(timeline_tweets_for_insert)
            print(f"Inserted timeline_tweets for {username}")
        except:
            print(twitter_url)
    print("Finish crawling timeline tweets!")
