from analysis.redis_queue import RedisQueue
from crawler import Crawler
import analysis.anal_postprocess as postprocess
import pprint
import analysis.db as db
tag_map = {
            '1h': 'popular-collections-1h', 
            '1d': 'popular-collections-1day', 
            '7d': 'popular-collections-7days', 
            '30d': 'popular-collections-30days',
            }

tags = [
  '1h', '1d', '7d', '30d']

collection_crawler = Crawler()
queue = RedisQueue()
NFT = 'nft'
ANAL = 'anal'
pprint = pprint.PrettyPrinter()
if __name__ == '__main__':
    dummy_json = {
        'key': 'dummy'
    }
    queue.delete(NFT)
    queue.delete(ANAL)
    while True:
        if queue.is_empty(NFT) and queue.is_empty(ANAL):
          print("Crawling...")
          all_me_collections_by_tags = collection_crawler.get_all_me_collections_by_tags(tags)
          print("Finish crawl popular collections!")
          upcoming_collections = collection_crawler.get_top_upcoming_collection()
          print("Finish crawl upcoming collections!")

          request_upcoming = {'request-upcoming': list(db.get_collection('dashboarditems').find({'tag': 'request-upcoming'}))}
          request_me = {'request-me': list(db.get_collection('dashboarditems').find({'tag': 'request-me'}))}
          
          all_collections = {
              **all_me_collections_by_tags,
              **upcoming_collections,
              **request_upcoming,
              **request_me
          }
          all_cols_for_db = postprocess.process_all_collections_for_db(all_collections)
          
          queue.lpush_many(NFT, all_cols_for_db)
          queue.expire(NFT)
          print(f"Key {NFT} expires in {queue.ttl(NFT)}")
          print(f'Enqueues {len(all_cols_for_db)} collections to (Key: {NFT}) redis queue!')

          db.drop_all_then_insert_many(all_cols_for_db, 'all_nfts')

          print(f"Remove old and insert new collections to all_nft!")
