import httpx

import api_common
import api_1_1
import api_2
import api_graph
import config
import redis_decorator
import authman


@redis_decorator.cache(ttl_secs=60*15)
def get_guest_token():
    return request(api_1_1.guest_token()).json()["guest_token"]


def gen_guest_token_headers():
    return {"x-guest-token": get_guest_token()}

auth_man = authman.AuthManager([api_common.gen_authenticated_headers_base(auth) for auth in config.auth], gen_guest_token_headers)

def add_base_request_params(params):
    params['headers'] = params.get('headers', {}) | api_common.gen_headers_base()
    params['method'] = params.get('method', 'get')

def request(params):
    add_base_request_params(params)
    resp = httpx.request(**params)
    resp.raise_for_status()
    return resp

def request_as_guest(params):
    params['headers'] = params.get('headers', {}) | gen_guest_token_headers()
    resp = request(params)
    if resp.headers['x-rate-limit-remaining'] == '1':
        get_guest_token.invalidate_cache()
    return resp

def request_as_user(params):
    add_base_request_params(params)

    while True:
        params['headers'] = params.get('headers', {}) | auth_man.get()
        resp = httpx.request(**params)
        if resp.status_code == 429:
            auth_man.block_last()
            continue
        resp.raise_for_status()
        return resp


@redis_decorator.cache(ttl_secs=60*60*24)
def get_user(username):
    return request_as_guest(api_graph.user_by_screen_name(username)).json()

def get_user_id(username):
    user = get_user(username)
    return user['data']['user']['result']['rest_id']

@redis_decorator.cache(ttl_secs=60*60)
def get_likes(username, cursor=None):
    return request_as_user(api_graph.likes(get_user_id(username), cursor)).json()

def get_appropriate_request_func(username):
    user = get_user(username)
    if user['data']['user']['result']['legacy']['possibly_sensitive']:
        return request_as_user
    return request_as_guest

@redis_decorator.cache(ttl_secs=60*60)
def get_user_tweets(username, cursor=None):
    request_func = get_appropriate_request_func(username)
    return request_func(api_graph.user_tweets(get_user_id(username), cursor)).json()

@redis_decorator.cache(ttl_secs=60*60)
def get_tweet(tweet_id, username, cursor=None):
    request_func = get_appropriate_request_func(username)
    return request_func(api_graph.tweet_detail(tweet_id, cursor)).json()


@redis_decorator.cache(ttl_secs=60*60)
def get_favoriters(tweet_id, cursor=None):
    return request_as_user(api_graph.favoriters(tweet_id, cursor)).json()

@redis_decorator.cache(ttl_secs=60*60)
def get_retweeters(tweet_id, cursor=None):
    return request_as_user(api_graph.retweeters(tweet_id, cursor)).json()

@redis_decorator.cache(ttl_secs=60*60)
def search(query, cursor=None):
    try:
        return {
            'search': request_as_user(api_graph.search(query, cursor)).json(),
            'version': 'graphql'
        }
    except httpx.HTTPStatusError:
        #TODO implement cursor
        return {
            'search': request_as_user(api_2.search(query)).json(),
            'version': '2'
        }
