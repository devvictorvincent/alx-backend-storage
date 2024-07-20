#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''

import redis
import uuid

class Cache:
     '''An object for storing data in a Redis data storage.
    '''
    def  __init__(self):
        self._redis = redis.Redis()
        self._redis.flushall()

    def store(self, data):
        '''Stores a value in a Redis data storage and returns the key.
        '''
        guid = str(uuid.uuid1());
        self._redis.set(guid, data)
        return guid

