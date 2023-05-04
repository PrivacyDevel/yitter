import traceback

accent_color = 'darkgreen'

def render_user(user):
    html = ''
    html += f"<a href='/{user['screen_name']}'>"
    html += f"<img src='{user['profile_image_url_https']}'>"
    html += '@' + user['screen_name']
    html += '<h2>' + user['name'] + '</h2>'
    html += '</a>'
    return html

def render_tweet(tweet, user, views=None):

    tweet_link = f"/{user['screen_name']}/status/{tweet['id_str']}"

    html = '<div style="background:#111111;padding:20px;margin-bottom:10px;padding-top:5px">'
    html += f"<a href='{tweet_link}'><p>{tweet['created_at']}</p></a>"
    html += render_user(user)
    if 'retweeted_status_result' in tweet:
        html += render_user(tweet['retweeted_status_result']['result']['core']['user_results']['result']['legacy'])
        tweet = tweet['retweeted_status_result']['result']['legacy']
        text = tweet['full_text']
    elif 'full_text' in tweet:
        text = tweet['full_text']
    else:
        text = tweet['text']
    html += '<p>' + text + '</p>'

    try:
        for media in tweet['extended_entities']['media']:
            url = media['media_url_https']
            if media['type'] == 'video':
                html += f"<video poster='{url}' controls style='max-height:512px;max-width:100%'>"
                for variant in media['video_info']['variants']:
                    html += f"<source src='{variant['url']}' type='{variant['content_type']}'>"
                html += '</video>'
            else:
                html += f'<a href="{url}"><img src="{url}" style="max-height:512px;max-width:100%"></a>'

    except KeyError:
        pass

    html += f"<a href='{tweet_link}' style='display:flex;margin-top:10px;align-items:center;transform:translateX(-10px)'>"

    try:
        html += f"<img src='/static/message-reply.svg' class=icon>{tweet['reply_count']}"
    except KeyError:
        pass

    html += f"<img src='/static/repeat-variant.svg' class=icon>{tweet['retweet_count']}"
    html += f"<img src='/static/thumb-up.svg' class=icon>{tweet['favorite_count']}"

    if views is not None:
        html += f"<img src='/static/eye-outline.svg' class=icon>{views}"

    html += '</a>'
    html += '</div>'
    
    return html


def render_graph_tweet(content):
    result = content['itemContent']['tweet_results']['result']
    tweet = result['legacy']
    user = result['core']['user_results']['result']['legacy']
    
    views = None
    try:
        views = result['views']['count']
    except KeyError:
        pass

    return render_tweet(tweet, user, views)

def render_load_more(content):
    return f"<a href='?cursor={content['value']}'>load more</a>"


def render_instruction(entry):
    html = ''
    content = entry['content']
    if 'itemContent' in content:
        itemContent = content['itemContent']
        if 'tweet_results' in itemContent:
            html += render_graph_tweet(content)
        else:
            try:
                html += render_load_more(itemContent)
            except KeyError:
                traceback.print_exc()
    if 'items' in content:
        html += '<div style="position:relative">'
        html += f"<div style='position:absolute;height:100%;width:5px;background:{accent_color}'></div>"
        for item in content['items']:
            try:
                html += render_graph_tweet(item['item'])
            except KeyError:
                traceback.print_exc()
        html += '</div>'
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

def render_user_header(user):
    user = user['data']['user']['result']['legacy']
    username = user['screen_name']
    html = '<div style="background:#111111;padding:20px;margin-bottom:20px">'
    html += f"<title>{user['name']} (@{username}) - yitter</title>"
    html += render_user(user)
    html += '<p>' + user['description'] + '</p>'
    html += f'<ul><li><a href="/{username}">Home</a></li><li><a href="/{username}/favorites">Likes</a></li></ul>'
    html += '</div>'
    return html

def render_top():
    html = '<style>body{background:black;color:white}a{color:' + accent_color + ';text-decoration:none}.icon{height:24px;filter:invert(100%);margin-right:5px;margin-left:10px}</style>'
    html += '<link rel="icon" href="/static/head.webp">'
    html += '<div style="margin:auto;width:50%">'
    html += '<div style="display:flex">'
    html += f"<h1 style='margin:auto;display:block;color:{accent_color}'>yitter</h1>"
    html += '</div>'
    html += '<div style="height:64px;display:flex">'
    html += '<img src="/static/head.webp" style="height:64px;float:left">'
    html += '<form action="/search" style="margin:auto;display:block"><input name="q"><input type="submit" value="search"></form>'
    html += '<img src="/static/head.webp" style="height:64px;float:right;transform:scaleX(-1);">'
    html += '</div>'
    return html
