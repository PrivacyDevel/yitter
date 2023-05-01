import requests

import api_common
import api_1_1
import api_graph
import config
import redis_decorator


def request(**kwargs):
    kwargs['headers'] = kwargs.get('headers', {}) | api_common.gen_headers_base()
    kwargs['method'] = kwargs.get('method', 'get')
    resp = requests.request(**kwargs)
    resp.raise_for_status()
    return resp

def request_as_guest(**kwargs):
    kwargs['headers'] = kwargs.get('headers', {}) | {"x-guest-token": get_guest_token()}
    resp = request(**kwargs)
    if resp.headers['x-rate-limit-remaining'] == '0':
        get_guest_token.invalidate_cache()
    return resp

def request_as_user(**kwargs):
    #TODO do user rotation
    kwargs['headers'] = kwargs.get('headers', {}) | api_common.gen_authenticated_headers_base(config.auth[1])
    return request(**kwargs)


@redis_decorator.cache(ttl_secs=60*15)
def get_guest_token():
    return request(**api_1_1.guest_token()).json()["guest_token"]

@redis_decorator.cache(ttl_secs=60*60*24)
def get_user(username):
    return request_as_guest(**api_graph.user_by_screen_name(username)).json()

def get_user_id(username):
    user = get_user(username)
    return user['data']['user']['result']['rest_id']

@redis_decorator.cache(ttl_secs=60*60)
def get_likes(username, cursor=None):
    return request_as_user(**api_graph.likes(get_user_id(username), cursor)).json()

@redis_decorator.cache(ttl_secs=60*60)
def get_user_tweets(username, cursor=None):
    user = get_user(username)
    if user['data']['user']['result']['legacy']['possibly_sensitive']:
        request_func = request_as_user
    else:
        request_func = request_as_guest
    return request_func(**api_graph.user_tweets(get_user_id(username), cursor)).json()

@redis_decorator.cache(ttl_secs=60*60)
def get_tweet(tweet_id, username, cursor=None):
    user = get_user(username)
    if user['data']['user']['result']['legacy']['possibly_sensitive']:
        request_func = request_as_user
    else:
        request_func = request_as_guest
    return request_func(**api_graph.tweet_detail(tweet_id, cursor)).json()

