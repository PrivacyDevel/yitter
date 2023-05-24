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
    html += html_renderer.render_instructions(tweets['data']['user']['result']['timeline']['timeline'])
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
    html += html_renderer.render_instructions(tweet['data']['threaded_conversation_with_injections'])
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
    search = api.search(query, bottle.request.params.get('cursor'))
    if search['version'] == 'graphql':
        html += html_renderer.render_instructions(search['search']['data']['search_by_raw_query']['search_timeline']['timeline'], {'q': query})
    else:
        for tweet in search['globalObjects']['tweets'].values():
            html += html_renderer.render_tweet(tweet, search['search']['globalObjects']['users'][tweet['user_id_str']])
    return html

@bottle.get('/')
def landing():
    html = ''
    html += '<title>yitter</title>'
    html += '<div style="height:100%">'
    html += '<div style="position:relative;top:50%;transform:translateY(-50%)">'
    html += html_renderer.render_top()
    return html

@bottle.get('/<username>/status/<tweet_id>/favoriters')
def favoriters(username, tweet_id):
    html = ''
    html += '<title>yitter</title>'
    html += html_renderer.render_top()
    likers = api.get_favoriters(tweet_id, bottle.request.params.get('cursor'))
    html += html_renderer.render_instructions(likers['data']['favoriters_timeline']['timeline'])
    return html


@bottle.get('/<username>/status/<tweet_id>/retweeters')
def retweeters(username, tweet_id):
    html = ''
    html += '<title>yitter</title>'
    html += html_renderer.render_top()
    retweeters = api.get_retweeters(tweet_id, bottle.request.params.get('cursor'))
    html += html_renderer.render_instructions(retweeters['data']['retweeters_timeline']['timeline'])
    return html

bottle.run(server=config.SERVER, port=config.BIND_PORT, host=config.BIND_ADDRESS)
