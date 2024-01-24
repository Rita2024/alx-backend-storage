#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import requests
import time
from functools import wraps

CACHE = {}

def cache_decorator(expiration_time=10):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            key = f"count:{url}"

            if key in CACHE and time.time() - CACHE[key]['timestamp'] < expiration_time:
                return CACHE[key]['content']

            result = func(url)
            CACHE[key] = {'content': result, 'timestamp': time.time()}
            return result

        return wrapper

    return decorator

@cache_decorator()
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

# Example usage:
slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
print(get_page(slow_url))  # This will be slow due to the simulated delay

# Accessing the same URL again within 10 seconds should retrieve the cached result
print(get_page(slow_url))

# Accessing a different URL
another_url = "http://www.example.com"
print(get_page(another_url))

# After 10 seconds, accessing the slow URL again will trigger a new request and update the cache
time.sleep(10)
print(get_page(slow_url))
