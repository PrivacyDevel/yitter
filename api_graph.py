import json

base_url = "https://twitter.com/i/api/graphql/"

def gen_features_base():
    return {
        "responsive_web_graphql_exclude_directive_enabled": True,
        "blue_business_profile_image_shape_enabled": False,
        "verified_phone_label_enabled": False,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False, # no effect found
        "responsive_web_graphql_timeline_navigation_enabled": False # no effect found
    }

def gen_features_base_ext():
    return gen_features_base() | {
        "longform_notetweets_consumption_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled" : False,
        "tweet_awards_web_tipping_enabled" : False,
        "tweetypie_unmention_optimization_enabled": True, # False = unmention_info, True = unmention_data
        "responsive_web_edit_tweet_api_enabled" : False, # edits on twitter?
        "freedom_of_speech_not_reach_fetch_enabled" : False, # no effect found
        "vibe_api_enabled" : False, # no effect found
        "standardized_nudges_misinfo": False, # no effect found
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled" : False, # no effect found
        "interactive_text_enabled": False, # no effect found
        "responsive_web_enhance_cards_enabled" : False, # no effect found
        "responsive_web_text_conversations_enabled" : False # no effect found
    }

def user_by_screen_name(username):

    variables = {
            "screen_name": username,
    }

    return {"url": base_url + "k26ASEiniqy4eXMdknTSoQ/UserByScreenName", "params": {"variables": json.dumps(variables), "features": json.dumps(gen_features_base())}}

def likes(user_id, cursor=None, count=20):

    variables = {
        "userId": user_id,
        "count": count,
        "withDownvotePerspective": False,
        "includePromotedContent": False, # no effect found
        "withReactionsMetadata": False, # no effect found
        "withReactionsPerspective": False, # no effect found
    }

    if cursor is not None:
        variables['cursor'] = cursor
    
    features = gen_features_base_ext() | {
        "longform_notetweets_richtext_consumption_enabled": False #TODO consider implementing. Example tweet id: 1649150616063602693
    }

    return {"url": base_url + "fN4-E0MjFJ9Cn7IYConL7g/Likes", "params": {"variables": json.dumps(variables), "features": json.dumps(features)}}

def user_tweets(user_id, cursor=None, count=40):

    variables = {
        "userId" : user_id,
        "count" : count,
        "includePromotedContent": False, # no effect found
        "withVoice" : False # no effect found
    }

    if cursor is not None:
        variables['cursor'] = cursor

    features = gen_features_base_ext() | {
        "longform_notetweets_rich_text_read_enabled" : False #TODO consider implementing. Example tweet id: 1649150616063602693
    }

    return {"url": base_url + "CdG2Vuc1v6F5JyEngGpxVw/UserTweets", "params": {"variables": json.dumps(variables), "features": json.dumps(features)}}
    
def tweet_detail(tweet_id, cursor=None):

    variables = {
        "focalTweetId": tweet_id,
        "withBirdwatchNotes": False,
        "includePromotedContent": False, # no effect found
        "withVoice" : False # no effect found
    }

    if cursor is not None:
        variables['cursor'] = cursor

    features = gen_features_base_ext() | {
        "longform_notetweets_rich_text_read_enabled": False #TODO consider implementing. Example tweet id: 1649150616063602693
    }

    return {"url": base_url + "BbCrSoXIR7z93lLCVFlQ2Q/TweetDetail", "params": {"variables": json.dumps(variables), "features": json.dumps(features)}}

def search(query, cursor=None, count=20):

    variables = {
        "rawQuery": query,
        "count": count, # optional
        "product": "Latest",
    }

    if cursor is not None:
        variables['cursor'] = cursor

    features = gen_features_base_ext() | {
        "longform_notetweets_rich_text_read_enabled": True #TODO consider implementing. Example tweet id: 1649150616063602693
    }

    return {"url": base_url + "gkjsKepM6gl_HmFWoWKfgg/SearchTimeline", "params": {"variables": json.dumps(variables), "features": json.dumps(features)}}

def favoriters(tweet_id, cursor=None, count=20):

    variables = {
        "tweetId" : tweet_id,
        "count" : count,
        "includePromotedContent": False, # no effect found
    }

    if cursor is not None:
        variables['cursor'] = cursor

    features = gen_features_base_ext() | {
        "longform_notetweets_rich_text_read_enabled": True, #TODO consider implementing. Example tweet id: 1649150616063602693
        "rweb_lists_timeline_redesign_enabled": False, # no effect found
        "creator_subscriptions_tweet_preview_api_enabled": False, # no effect found
        "longform_notetweets_inline_media_enabled": True # no effect found
    }

    return {"url": base_url + "mDc_nU8xGv0cLRWtTaIEug/Favoriters", "params": {"variables": json.dumps(variables), "features": json.dumps(features)}}
