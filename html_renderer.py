import traceback
import urllib.parse
import re

accent_color = 'darkgreen'


def extend_text(text, urls_container):
    for url in urls_container['urls']:
        text = text.replace(url['url'], f"<a href='{url['expanded_url']}'>{url['expanded_url']}</a>")
    text = re.sub(r'@(\S+)', r'<a href="/\1">@\1</a>', text)
    return text


def render_user(user):
    html = ''
    html += f"<a href='/{user['screen_name']}' class=icon-container>"
    html += f"<img src='{user['profile_image_url_https']}'>"
    html += '<div style="display:inline;margin-left:5px">'
    html += f"<h2 style='margin:0px'>{user['name']}</h2>"
    html += '@' + user['screen_name']
    html += '</div>'
    html += '</a>'
    return html

def render_tweet(tweet, user, graph_tweet=None, is_pinned=False):

    html = '<div style="background:#111111;padding:20px;margin-bottom:10px;padding-top:5px">'

    if 'retweeted_status_result' in tweet:
        graph_retweeted = tweet['retweeted_status_result']['result']
        if 'tweet' in graph_retweeted:
            graph_retweeted = graph_retweeted['tweet']
        retweeted = graph_retweeted['legacy']

        retweeted_user = graph_retweeted['core']['user_results']['result']['legacy']

        tweet_link = f"/{retweeted_user['screen_name']}/status/{retweeted['id_str']}"
    else:
        retweeted = None
        tweet_link = f"/{user['screen_name']}/status/{tweet['id_str']}"

    html += f"<a href='{tweet_link}'>"

    if is_pinned:
        html += '<p class=icon-container><img src="/static/pin.svg" class=icon>Pinned Tweet</p>'

    html += f"<p>{tweet['created_at']}</p></a>"
    html += render_user(user)
    if retweeted is not None:
        html += render_tweet(retweeted, retweeted_user, graph_retweeted)
        html += '</div>'
        return html

    if graph_tweet is not None and 'note_tweet' in graph_tweet:
        text = graph_tweet['note_tweet']['note_tweet_results']['result']['text']
    else:
        text = tweet.get('full_text', tweet.get('text'))
    text = extend_text(text, tweet['entities'])
    html += '<p>' + text + '</p>'

    try:
        for media in tweet['extended_entities']['media']:
            html = html.replace(media['url'], '')
            url = media['media_url_https']
            if media['type'] in ('video', 'animated_gif'):
                html += f"<video poster='{url}' style='max-height:512px;max-width:100%' "
                if media['type'] == 'video':
                    html += 'controls'
                else:
                    html += 'autoplay loop'
                html += '>'
                for variant in media['video_info']['variants']:
                    html += f"<source src='{variant['url']}' type='{variant['content_type']}'>"
                html += '</video>'
            else:
                html += f'<a href="{url}"><img src="{url}" style="max-height:512px;max-width:100%"></a>'

    except KeyError:
        pass

    if graph_tweet is not None and 'quoted_status_result' in graph_tweet:
        quoted_tweet_graph = graph_tweet['quoted_status_result']['result']
        quoted_tweet = quoted_tweet_graph['legacy']
        quoted_tweet_user = quoted_tweet_graph['core']['user_results']['result']['legacy']
        html += render_tweet(quoted_tweet, user, quoted_tweet_graph)

    html += f"<a href='{tweet_link}' class=icon-container>"

    try:
        html += f"<img src='/static/message-reply.svg' class=icon>{tweet['reply_count']}"
    except KeyError:
        pass

    html += f"<img src='/static/format-quote-close.svg' class=icon>{tweet['quote_count']}"
    html += f"<img src='/static/repeat-variant.svg' class=icon>{tweet['retweet_count']}"
    html += f"<img src='/static/thumb-up.svg' class=icon>{tweet['favorite_count']}"

    try:
        if graph_tweet is not None:
            html += f"<img src='/static/eye-outline.svg' class=icon>{graph_tweet['views']['count']}"
    except KeyError:
        pass

    html += '</a>'
    html += '</div>'

    return html


def render_graph_tweet(content, is_pinned):
    graph_tweet = content['itemContent']['tweet_results']['result']

    if 'tweet' in graph_tweet:
        graph_tweet = graph_tweet['tweet']
    tweet = graph_tweet['legacy']

    user = graph_tweet['core']['user_results']['result']
    if 'tweet' in user:
        user = user['tweet']
    user = user['legacy']

    return render_tweet(tweet, user, graph_tweet, is_pinned)

def render_load_more(content, params):
    params['cursor'] = content['value']
    href = urllib.parse.urlencode(params)
    return f"<a href='?{href}'>load more</a>"


def render_instruction(entry, params, is_pinned=False):
    html = ''
    content = entry['content']
    if 'itemContent' in content:
        itemContent = content['itemContent']
        if 'tweet_results' in itemContent:
            html += render_graph_tweet(content, is_pinned)
        else:
            try:
                html += render_load_more(itemContent, params)
            except KeyError:
                traceback.print_exc()
    if 'items' in content:
        html += '<div style="position:relative">'
        if len(content['items']) > 1:
            html += f"<div style='position:absolute;height:100%;width:5px;background:{accent_color}'></div>"

        for item in content['items']:
            try:
                html += render_graph_tweet(item['item'], is_pinned)
            except KeyError:
                traceback.print_exc()
        html += '</div>'
    if 'value' in content:
        html += render_load_more(content, params)

    return html

def render_instructions(timeline, params=None):

    if params is None:
        params = {}

    html = ''

    for instruction in timeline['instructions']:
        if 'entry' in instruction and instruction['type'] == 'TimelinePinEntry':
            html += render_instruction(instruction['entry'], params, True)

    for instruction in timeline['instructions']:
        if 'entries' in instruction:
            for entry in instruction['entries']:
                html += render_instruction(entry, params)
        if 'entry' in instruction and instruction['type'] != 'TimelinePinEntry':
            html += render_instruction(instruction['entry'], params)
    return html

def render_user_header(user):
    user = user['data']['user']['result']['legacy']
    username = user['screen_name']
    html = ''

    if 'profile_banner_url' in user:
        html += f"<a href='{user['profile_banner_url']}'><img src='{user['profile_banner_url']}' style='max-width:100%'></a>"

    html += '<div style="background:#111111;padding:20px;margin-bottom:20px">'
    html += f"<title>{user['name']} (@{username}) - yitter</title>"
    html += render_user(user)
    description = extend_text(user['description'], user['entities']['description'])
    html += '<p>' + description + '</p>'
    html += f'<a href="/{username}">Home</a> <a href="/{username}/favorites">Likes</a>'
    html += '</div>'
    return html

def render_top():
    html = '<style>body{background:black;color:white}a{color:' + accent_color + ';text-decoration:none}.icon{height:24px;filter:invert(100%);margin-right:5px;margin-left:10px}.icon-container{display:flex;margin-top:10px;align-items:center;transform:translateX(-10px)}</style>'
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
