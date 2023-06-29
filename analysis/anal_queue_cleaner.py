from redis_queue import RedisQueue
import time
from redis_queue import RedisQueue
import anal_postprocess as postpro
import pprint
import db

queue = RedisQueue()
NFT = 'nft'
ANAL = 'anal'

tag_map = {
            'new_collections': 'new-collections', 
            '1h': 'popular-collections-1h', 
            '1d': 'popular-collections-1day', 
            '7d': 'popular-collections-7days', 
            '30d': 'popular-collections-30days',
            }

tags = ['new_collections', '1h', '1d', '7d', '30d']
print("Queue cleaner is running ...!")
if __name__ == "__main__":
    start = time.time()
    while True:
        if queue.is_empty(NFT) and queue.is_empty(ANAL) == False:
            time.sleep(30)
            all_nfts_stat = queue.lrange(ANAL, 0, -1)

            db_tag = list(tag_map.values())
            nfts_by_tag = postpro.map_nfts_to_tag(all_nfts_stat, db_tag)
            for tag, nfts in nfts_by_tag.items():
                data_cols_by_tag = nfts_by_tag[tag]
                if len(data_cols_by_tag) > 0:
                    db.drop_then_insert(data_cols_by_tag, tag)
                    postpro.send_shock_to_discord(data_cols_by_tag)
            # db.drop_all_then_insert_many(analysis, COLLECTION_ANAL)
            queue.delete(ANAL)

            print(f'Finish analyze all collections in {(time.time() - start) / 60}')
            start = time.time()

