def render_user(user):
    html = ''
    html += f"<a href='/{user['screen_name']}'>"
    html += f"<img src='{user['profile_image_url_https']}'>"
    html += '@' + user['screen_name']
    html += '<h2>' + user['name'] + '</h2>'
    html += '</a>'
    return html

def render_tweet(tweet, user):
    html = '<div style="background:#111111;padding:20px;margin-bottom:20px">'
    html += f"<a href='/{user['screen_name']}/status/{tweet['id_str']}'><p>{tweet['created_at']}</p></a>"
    html += render_user(user)
    if 'retweeted_status_result' in tweet:
        html += render_user(tweet['retweeted_status_result']['result']['core']['user_results']['result']['legacy'])
        text = tweet['retweeted_status_result']['result']['legacy']['full_text']
    elif 'full_text' in tweet:
        text = tweet['full_text']
    else:
        text = tweet['text']
    html += '<p>' + text + '</p>'

    try:
        for media in tweet['entities']['media']:
            url = media['media_url_https']
            html += f'<a href="{url}"><img src="{url}" style="max-height:512px"></a>'
    except KeyError as e:
        print(e)
    
    html += '</div>'
    
    return html


def render_graph_tweet(content):
    result = content['itemContent']['tweet_results']['result']
    tweet = result['legacy']
    user = result['core']['user_results']['result']['legacy']
    return render_tweet(tweet, user)

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
            except KeyError as e:
                print(e)
    if 'items' in content:
        for item in content['items']:
            try:
                html += render_graph_tweet(item['item'])
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

def render_user_header(user):
    user = user['data']['user']['result']['legacy']
    username = user['screen_name']
    html = '<div style="background:#111111;padding:20px;margin-bottom:20px">'
    html += f"<title>{user['name']} (@{username}) - yitter</title>"
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
