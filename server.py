#!/usr/bin/env python3

import bottle

import api
import config

def render_user(result):
    html = ''
    user = result['core']['user_results']['result']['legacy']
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
    html += render_user(result)
    if 'retweeted_status_result' in tweet:
        html += render_user(tweet['retweeted_status_result']['result'])
        text = tweet['retweeted_status_result']['result']['legacy']['full_text']
        html += 'RT: <p>' + text + '</p>'
    else:
        text = tweet['full_text']
        html += 'Tweet: <p>' + text + '</p>'

    try:
        for media in tweet['entities']['media']:
            url = media['media_url_https']
            html += '<img src="' + url + '" style="max-height:512px">'
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
            html += render_load_more(itemContent)
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
    html = '<div style="margin:auto;width:50%">'
    for instruction in timeline['instructions']:
        if 'entries' in instruction:
            for entry in instruction['entries']:
                html += render_instruction(entry)
        if 'entry' in instruction:
            html += render_instruction(instruction['entry'])
    html += '</div>'
    return html

def render_user_header(username):
    html = ''
    user = api.get_user(username)
    html += '<h1>' + user['data']['user']['result']['legacy']['name'] + '</h1>'
    html += '<p>' + user['data']['user']['result']['legacy']['description'] + '</p>'
    html += f'<ul><li><a href="/{username}">Home</a></li><li><a href="/{username}/favorites">Likes</a></li></ul>'
    return html

def render_top():
    return '<style>body{background:black;color:white}a{color:darkgreen;text-decoration:none}</style>'


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
    tweets = api.get_likes(username)
    html += render_instructions(tweets['data']['user']['result']['timeline']['timeline'])
    return html

@bottle.get('/<username>/status/<tweet_id>')
def tweet(username, tweet_id):
    html = ''
    html += render_top()
    tweet = api.get_tweet(tweet_id, username)
    html += render_instructions(tweet['data']['threaded_conversation_with_injections_v2'])
    return html


bottle.run(server=config.SERVER, port=config.BIND_PORT, host=config.BIND_ADDRESS)
