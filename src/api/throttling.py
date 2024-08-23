import time
import functools
from collections import defaultdict
from flask import request, jsonify

# In-memory store for tracking requests (for simplicity, consider using Redis for production)
request_log = defaultdict(list)

def throttle(max_calls, period=60):
    """
    Throttle decorator to limit the number of requests from a user or IP address.
    
    :param max_calls: Maximum number of allowed calls within the period.
    :param period: Period of time (in seconds) in which the max_calls are counted.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            identifier = get_identifier()
            now = time.time()
            request_times = request_log[identifier]

            # Filter out requests that are outside the current time window
            request_times = [t for t in request_times if t > now - period]
            request_log[identifier] = request_times

            if len(request_times) >= max_calls:
                return jsonify({"error": "Too many requests, please try again later."}), 429

            # Add the current request time to the log
            request_log[identifier].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

def get_identifier():
    """
    Get a unique identifier for throttling.
    By default, this uses the client's IP address. Can be extended to use API keys or user IDs.
    """
    return request.remote_addr

def clear_request_logs():
    """
    Clear all request logs. Useful for testing or resetting the state.
    """
    global request_log
    request_log = defaultdict(list)

def throttle_by_ip(max_calls, period=60):
    """
    Throttle requests by IP address.
    
    :param max_calls: Maximum number of allowed calls within the period.
    :param period: Period of time (in seconds) in which the max_calls are counted.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            identifier = request.remote_addr
            now = time.time()
            request_times = request_log[identifier]

            request_times = [t for t in request_times if t > now - period]
            request_log[identifier] = request_times

            if len(request_times) >= max_calls:
                return jsonify({"error": "Too many requests from this IP, please try again later."}), 429

            request_log[identifier].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

def throttle_by_user(max_calls, period=60):
    """
    Throttle requests by user identifier (e.g., user ID or API key).
    
    :param max_calls: Maximum number of allowed calls within the period.
    :param period: Period of time (in seconds) in which the max_calls are counted.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            identifier = get_identifier()  # Modify this to get user ID or API key
            now = time.time()
            request_times = request_log[identifier]

            request_times = [t for t in request_times if t > now - period]
            request_log[identifier] = request_times

            if len(request_times) >= max_calls:
                return jsonify({"error": "Too many requests, please try again later."}), 429

            request_log[identifier].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator
