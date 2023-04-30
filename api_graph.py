import json

base_url = "https://twitter.com/i/api/graphql/"

def gen_features_base():
    return {
        "blue_business_profile_image_shape_enabled": False,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True
    }

def gen_features_base_ext():
    return gen_features_base() | {
        "view_counts_everywhere_api_enabled": True,
        "freedom_of_speech_not_reach_fetch_enabled" : True,
        "vibe_api_enabled" : True,
        "tweetypie_unmention_optimization_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled" : True,
        "responsive_web_edit_tweet_api_enabled" : True,
        "longform_notetweets_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled" : False,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled" : False,
        "interactive_text_enabled": True,
        "responsive_web_enhance_cards_enabled" : False,
        "responsive_web_text_conversations_enabled" : False,
    }

def user_by_screen_name(username):

    variables = {
            "screen_name": username,
    }

    return {"url": base_url + "k26ASEiniqy4eXMdknTSoQ/UserByScreenName", "params": {"variables": json.dumps(variables), "features": json.dumps(gen_features_base())}}

def likes(user_id, count=20):

    variables = {
        "userId": user_id,
        "count": count,
        "includePromotedContent": False,
        "withDownvotePerspective": False,
        "withReactionsMetadata": False,
        "withReactionsPerspective": False,
    }
    
    features = gen_features_base_ext() | {
        "longform_notetweets_richtext_consumption_enabled": False,
    }

    headers = {
        "content-type": "application/json",
    }

    return {"url": base_url + "fN4-E0MjFJ9Cn7IYConL7g/Likes", "params": {"variables": json.dumps(variables), "features": json.dumps(features)}, "headers": headers}

def user_tweets(user_id, cursor=None, count=40):

    variables = {
        "userId" : user_id,
        "count" : count,
        "includePromotedContent" : True,
        "withQuickPromoteEligibilityTweetFields" : True,
        "withV2Timeline" : True,
        "withVoice" : True
    }

    if cursor is not None:
        variables['cursor'] = cursor

    features = gen_features_base_ext() | {
        "longform_notetweets_rich_text_read_enabled" : True,
    }

    headers = {
        "content-type": "application/json",
    }

    return {"url": base_url + "CdG2Vuc1v6F5JyEngGpxVw/UserTweets", "params": {"variables": json.dumps(variables), "features": json.dumps(features)}, "headers": headers}
    
