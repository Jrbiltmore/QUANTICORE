from flask import Flask, request, jsonify
from functools import wraps
from redis import Redis
import time
import hashlib

# Initialize Redis for storing request counts and timestamps
redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)

def rate_limit(key_prefix, max_requests, period):
    """
    Rate limiting decorator to limit the number of requests.

    :param key_prefix: A prefix for Redis keys, typically specific to a route or resource.
    :param max_requests: Maximum number of allowed requests in the given period.
    :param period: Time period in seconds in which max_requests are counted.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = generate_key(key_prefix)
            current = int(time.time())
            pipeline = redis.pipeline()
            
            # Record a new request timestamp
            pipeline.zadd(key, {current: current})
            # Remove timestamps outside the rate limit period
            pipeline.zremrangebyscore(key, 0, current - period)
            # Get the total number of requests within the period
            pipeline.zcard(key)
            # Set the expiration time for the key
            pipeline.expire(key, period)
            requests_in_window = pipeline.execute()[-2]
            
            if requests_in_window > max_requests:
                return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

            return f(*args, **kwargs)
        return wrapped
    return decorator

def generate_key(key_prefix):
    """
    Generate a Redis key based on client IP and a key prefix.

    :param key_prefix: A prefix for the Redis key to differentiate between routes.
    :return: A string key unique to the client and route.
    """
    client_ip = request.remote_addr
    key = f"{key_prefix}:{client_ip}"
    # Optional: Further hash the key if needed to keep Redis keys concise
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def limit_global_requests(max_requests, period):
    """
    Rate limit decorator for globally limiting the number of requests from all clients.

    :param max_requests: Maximum number of allowed requests in the given period across all clients.
    :param period: Time period in seconds in which max_requests are counted.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = "global_rate_limit"
            current = int(time.time())
            pipeline = redis.pipeline()

            # Record a new request timestamp
            pipeline.zadd(key, {current: current})
            # Remove timestamps outside the rate limit period
            pipeline.zremrangebyscore(key, 0, current - period)
            # Get the total number of requests within the period
            pipeline.zcard(key)
            # Set the expiration time for the key
            pipeline.expire(key, period)
            requests_in_window = pipeline.execute()[-2]

            if requests_in_window > max_requests:
                return jsonify({"error": "Global rate limit exceeded. Try again later."}), 429

            return f(*args, **kwargs)
        return wrapped
    return decorator
