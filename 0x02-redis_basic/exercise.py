#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''

import redis
import uuid
from typing import Any, Callable, Optional, Union
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """ Decorator for Cache class methods to track call count
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """ Wraps called method and adds its call count redis before execution
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    '''An object for storing data in a Redis data storage.
    '''
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.
        '''
        guid = str(uuid.uuid4());
        self._redis.set(guid, data)
        return guid
    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        ''' Gets keys value from redis and converts
            result into correct data type
        '''
        redis = self._redis
        value = redis.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value
    def get_int(self, data: bytes) -> int:
        ''' Converts bytes to integers
        '''
        return int(data)
    def get_str(self, data: bytes) -> str:
        ''' Converts bytes to Strings
        '''
        return data.decode('utf-8')


