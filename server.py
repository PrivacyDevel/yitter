#!/usr/bin/env python3

import bottle

import api
import config

def render_user(user):
    html = ''
    html += f"<a href='/{user['screen_name']}'>"
    html += f"<img src='{user['profile_image_url_https']}'>"
    html += '@' + user['screen_name']
    html += '<h2>' + user['name'] + '</h2>'
    html += '</a>'
    return html


def render_tweet(content):
    html = '<div style="background:#111111;padding:20px;margin-bottom:20px">'
    result = content['itemContent']['tweet_results']['result']
    tweet = result['legacy']
    html += f"<a href='/{result['core']['user_results']['result']['legacy']['screen_name']}/status/{tweet['id_str']}'><p>{tweet['created_at']}</p></a>"
    html += render_user(result['core']['user_results']['result']['legacy'])
    if 'retweeted_status_result' in tweet:
        html += render_user(tweet['retweeted_status_result']['result']['core']['user_results']['result']['legacy'])
        text = tweet['retweeted_status_result']['result']['legacy']['full_text']
    else:
        text = tweet['full_text']
    html += '<p>' + text + '</p>'

    try:
        for media in tweet['entities']['media']:
            url = media['media_url_https']
            html += f'<a href="{url}"><img src="{url}" style="max-height:512px"></a>'
    except KeyError as e:
        print(e)
    
    html += '</div>'
    
    return html

def render_load_more(content):
    return f"<a href='?cursor={content['value']}'>load more</a>"


def render_instruction(entry):
    html = ''
    content = entry['content']
    if 'itemContent' in content:
        itemContent = content['itemContent']
        if 'tweet_results' in itemContent:
            html += render_tweet(content)
        else:
            try:
                html += render_load_more(itemContent)
            except KeyError as e:
                print(e)
    if 'items' in content:
        for item in content['items']:
            try:
                html += render_tweet(item['item'])
            except KeyError as e:
                print(e)
    if 'value' in content:
        html += render_load_more(content)

    return html

def render_instructions(timeline):
    html = ''
    for instruction in timeline['instructions']:
        if 'entries' in instruction:
            for entry in instruction['entries']:
                html += render_instruction(entry)
        if 'entry' in instruction:
            html += render_instruction(instruction['entry'])
    return html

def render_user_header(username):
    html = '<div style="background:#111111;padding:20px;margin-bottom:20px">'
    user = api.get_user(username)
    user = user['data']['user']['result']['legacy']
    html += f"<title>{user['name']} (@{user['screen_name']}) - yitter</title>"
    html += render_user(user)
    html += '<p>' + user['description'] + '</p>'
    html += f'<ul><li><a href="/{username}">Home</a></li><li><a href="/{username}/favorites">Likes</a></li></ul>'
    html += '</div>'
    return html

def render_top():
    html = '<style>body{background:black;color:white}a{color:darkgreen;text-decoration:none}</style>'
    html += '<link rel="icon" href="/static/head.webp">'
    html += '<div style="margin:auto;width:50%">'
    html += '<div style="height:64px;display:flex">'
    html += '<img src="/static/head.webp" style="height:64px;float:left">'
    html += '<h1 style="display:inline;color:darkgreen;margin:auto">yitter</h1>'
    html += '<img src="/static/head.webp" style="height:64px;float:right;transform:scaleX(-1);">'
    html += '</div>'
    return html


@bottle.get('/<username>')
def user(username):
    html = ''
    html += render_top()
    html += render_user_header(username)
    tweets = api.get_user_tweets(username, bottle.request.params.get('cursor'))
    html += render_instructions(tweets['data']['user']['result']['timeline_v2']['timeline'])
    return html


@bottle.get('/<username>/favorites')
def favorites(username):
    html = ''
    html += render_top()
    html += render_user_header(username)
    tweets = api.get_likes(username, bottle.request.params.get('cursor'))
    html += render_instructions(tweets['data']['user']['result']['timeline']['timeline'])
    return html

@bottle.get('/<username>/status/<tweet_id>')
def tweet(username, tweet_id):
    html = ''
    html += '<title>yitter</title>'
    html += render_top()
    tweet = api.get_tweet(tweet_id, username, bottle.request.params.get('cursor'))
    html += render_instructions(tweet['data']['threaded_conversation_with_injections_v2'])
    return html

@bottle.get('/static/<file>')
def static(file):
    return bottle.static_file(file, 'public')

bottle.run(server=config.SERVER, port=config.BIND_PORT, host=config.BIND_ADDRESS)
