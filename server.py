#!/usr/bin/env python3

import bottle

import api
import config
import html_renderer


@bottle.get('/<username>')
def user(username):
    html = ''
    html += html_renderer.render_top()
    user = api.get_user(username)
    html += html_renderer.render_user_header(user)
    tweets = api.get_user_tweets(username, bottle.request.params.get('cursor'))
    html += html_renderer.render_instructions(tweets['data']['user']['result']['timeline_v2']['timeline'])
    return html

@bottle.get('/<username>/favorites')
def favorites(username):
    html = ''
    html += html_renderer.render_top()
    user = api.get_user(username)
    html += html_renderer.render_user_header(user)
    tweets = api.get_likes(username, bottle.request.params.get('cursor'))
    html += html_renderer.render_instructions(tweets['data']['user']['result']['timeline']['timeline'])
    return html

@bottle.get('/<username>/status/<tweet_id>')
def tweet(username, tweet_id):
    html = ''
    html += '<title>yitter</title>'
    html += html_renderer.render_top()
    tweet = api.get_tweet(tweet_id, username, bottle.request.params.get('cursor'))
    html += html_renderer.render_instructions(tweet['data']['threaded_conversation_with_injections_v2'])
    return html

@bottle.get('/static/<file>')
def static(file):
    return bottle.static_file(file, 'public')

@bottle.get('/search')
def search():
    html = ''
    query = bottle.request.params.get('q')
    html += f'<title>"{query}" search - yitter</title>'
    html += html_renderer.render_top()
    search = api.search(query)
    for tweet in search['globalObjects']['tweets'].values():
        html += html_renderer.render_tweet(tweet, search['globalObjects']['users'][tweet['user_id_str']])
    return html

bottle.run(server=config.SERVER, port=config.BIND_PORT, host=config.BIND_ADDRESS)
