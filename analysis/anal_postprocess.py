tag_map = {
            'new_collections': 'new-collections', 
            '1h':'popular-collections-1h', 
            '1d': 'popular-collections-1day', 
            '7d': 'popular-collections-7days', 
            '30d': 'popular-collections-30days',
            }

def process_all_collections_for_db(tag_to_data):
  name_map = {}
  for me_tag, data in tag_to_data.items():
    db_tag = tag_map[me_tag]
    for nft_info in data:
      name = nft_info['name']
      if name not in name_map:
        if '_id' in nft_info: nft_info.pop('_id')

        name_map[name] = {
          **nft_info,
          'tags': set([db_tag])
        }
      else:
        tag_set = name_map[name]['tags']
        tag_set.add(db_tag)

  #convert tag set to list of tags
  for nft_info in name_map.values():
    nft_info['tags'] = list(nft_info['tags'])
  
  return list(name_map.values())


def map_nfts_to_tag(all_nfts_stat, tags):
  nft_map = {tag: [] for tag in tags}
  
  for nft in all_nfts_stat:
    for tag in nft['tags']:
      if '_id' in nft: nft.pop('_id')
      col_info = {
                    **nft,
                    'tag': tag
                }
        
      nft_map[tag].append(col_info)
  
  return nft_map
