from redis import Redis
import json
from ast import literal_eval

class RedisQueue:
    def __init__(self, host='redis-10229.c228.us-central1-1.gce.cloud.redislabs.com', port=10229):
        self.host = host
        self.port = port
        self.client = Redis(host=self.host, port=self.port, password='Tb3f2iVs8FNUY4dC2nGpwKG6ViegOW0U')
        self.expiration = 60 * 60 * 24 * 1000

    def convert_byte_to_json(self, byte_str):
        return json.loads(byte_str)

    def convert_json_to_byte(self, json_obj):
        return json.dumps(json_obj)

    def lpush_many(self, key, json_list):
        byte_string_list = [self.convert_json_to_byte(json_obj) for json_obj in json_list]
        return self.client.lpush(key, *byte_string_list)

    def lpush_one(self, key, json_obj):
        byte_string = self.convert_json_to_byte(json_obj)
        return self.client.lpush(key, byte_string)
    
    def rpop(self, key):
        pop = self.client.rpop(key)
        
        return self.convert_byte_to_json(pop) if pop != None else None

    def peek(self, key):
        return self.convert_byte_to_json(self.client.lrange(key, -1, -1))

    def is_empty(self, key):
        if self.client.lrange(key, -1, -1) == []:
            return True
        else:
            return False
    
    def lrange(self, key, start, end):
        byte_strings = self.client.lrange(key, start, end)
        return [self.convert_byte_to_json(byte_str) for byte_str in byte_strings]

    def peek(self, key):
        return self.lrange(key, -1, -1)[0]
    
    def delete(self, key):
        return self.client.delete(key)

    def ttl(self, key):
        return self.client.pttl(key) / 1000

    def expire(self, key, time=60 * 60 * 24):
        if self.exists(key):
            self.client.expire(key, time)
            return time
        else:
            return -1

    def exists(self, key):
        return self.client.exists(key)

